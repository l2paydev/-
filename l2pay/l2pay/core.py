import os
import json
import requests
from l2pay.settings import PRIVATE_KEY
import logging
import celery
from celery import shared_task
from datetime import datetime, timedelta

from .models import Payments, Transfer, Settings, UserBalance
from .serializer import PaymentsSerializer
from django.db.models import Sum
from django.db import models, connection, DatabaseError

logger = logging.getLogger(__name__)


class BaseTaskWithRetry(celery.Task):
    autoretry_for = (Exception,)
    retry_kwargs = {"max_retries": 10}
    retry_backoff = True


@shared_task(base=BaseTaskWithRetry)
def verify_payment_on_expiration(paymentId):
    payment = Payments.objects.filter(id=paymentId).first()
    if payment:
        logger.info(f"verify_payment_on_expiration {paymentId}")
        if payment.state != Payments.StateChoices.SUCCEED:
            mark_payment_as_expired(payment)
        pass


def mark_payment_as_expired(payment: Payments):
    utc_now = datetime.utcnow()
    payment.state = Payments.StateChoices.EXPIRED
    payment.updated_at = utc_now
    payment.save()
    notify_update_payment.delay(payment.id)


@shared_task(base=BaseTaskWithRetry)
def tracking_payment_pay_address(paymentId):
    payment = Payments.objects.filter(id=paymentId).first()
    if payment:
        logger.info(
            f"tracking_payment_pay_address {paymentId}, address {payment.pay_wallet}"
        )
        if (
            payment.state == Payments.StateChoices.OPEN
            or payment.state == Payments.StateChoices.PROCESSING
        ):
            transfers = []
            try:
                query = "SELECT transaction_hash, amount FROM transfers WHERE to_address = %s and symbol= %s"
                with connection.cursor() as cursor:
                    cursor.execute(query, [payment.pay_wallet, payment.currency])
                    transfers = cursor.fetchall()
            except DatabaseError as e:
                print(f"An error occurred: {e}")

            total_amount = 0  # Initialize the total amount
            transaction_hashs = []
            for transaction_hash, amount in transfers:
                total_amount += amount
                transaction_hashs.append(transaction_hash)

            # total_amount = Transfer.objects.filter(
            #     to_address=payment.pay_wallet, symbol=payment.currency
            # ).aggregate(total_amount=Sum("amount"))["total_amount"]
            if total_amount and total_amount >= payment.value:
                txhs = ",".join(transaction_hashs)

                utc_now = datetime.utcnow()
                payment.state = Payments.StateChoices.SUCCEED
                payment.updated_at = utc_now
                payment.tx_hash = txhs
                payment.save()
                notify_update_payment.delay(paymentId)
                balance = UserBalance.objects.filter(
                    currency=payment.currency,
                    network=payment.network,
                    user_id=payment.user.id,
                ).first()
                if balance:
                    balance.value += payment.value
                    balance.updated_at = utc_now
                    balance.save()
                else:
                    UserBalance.objects.create(
                        user=payment.user,
                        currency=payment.currency,
                        network=payment.network,
                        value=payment.value,
                    )


@shared_task(base=BaseTaskWithRetry)
def notify_update_payment(paymentId):
    payment = Payments.objects.filter(id=paymentId).first()
    if payment:
        logger.info(f"notify_update_payment {paymentId}")
        setting = Settings.objects.filter(user_id=payment.user.pk).first()
        if setting and setting.webhook_url:
            payment_data = PaymentsSerializer(instance=payment).data
            logger.info(f"notify payment {payment_data}")
            # Define the headers for the POST request
            headers = {"Content-Type": "application/json"}
            try:
                response = requests.post(
                    setting.webhook_url, data=json.dumps(payment_data), headers=headers
                )
            except:
                pass


@shared_task(base=BaseTaskWithRetry)
def periodict_track_open_payments():
    logger.info(f"periodict_track_open_payments")
    import pytz

    timezone = pytz.timezone("UTC")
    utcnow = timezone.localize(datetime.utcnow())
    payments = Payments.objects.filter(
        state__in=(Payments.StateChoices.OPEN, Payments.StateChoices.PROCESSING)
    )
    for payment in payments:
        if payment.expired_at <= utcnow:
            mark_payment_as_expired(payment)
        else:
            tracking_payment_pay_address.delay(payment.pk)
