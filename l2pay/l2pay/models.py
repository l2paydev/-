from django.db import models
from django.contrib.auth.models import User
from rest_framework_api_key.models import AbstractAPIKey, BaseAPIKeyManager


class Settings(models.Model):
    webhook_url = models.CharField(max_length=200, null=False)
    payout_address = models.CharField(max_length=200, null=True, default="")
    updated_at = models.DateTimeField(auto_now_add=True, auto_created=True, null=False)
    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE, related_name="setting"
    )

    class Meta:
        db_table = "settings"
        verbose_name = "Settings"
        verbose_name_plural = "Settings"


class APIKey(models.Model):
    key = models.CharField(max_length=100, null=False, db_index=True)
    secret = models.CharField(max_length=100, null=False, db_index=True)
    enabled = models.BooleanField(default=True, db_index=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="apikeys")

    class Meta:
        db_table = "apikeys"
        verbose_name = "APIKeys"
        verbose_name_plural = "APIKeys"

    pass


class MerchantAPIKeyManager(BaseAPIKeyManager):
    pass


class MerchantKey(AbstractAPIKey):
    objects = MerchantAPIKeyManager()

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="merchant_keys",
    )

    class Meta(AbstractAPIKey.Meta):
        verbose_name = "Merchant API key"
        verbose_name_plural = "Merchant API keys"


class Payments(models.Model):

    class NetworkChoices(models.TextChoices):
        Starknet = "Starknet"
        zkSync = "zkSync"
        XLAYER = "XLAYER"
        Kakarot = "KakarotZkEVM"
        Blast = "Blast"

    class StateChoices(models.TextChoices):
        OPEN = "OPEN"
        PROCESSING = "PROCESSING"
        SUCCEED = "SUCCEED"
        EXPIRED = "EXPIRED"

    class CurrencyChoices(models.TextChoices):
        USDT = "USDT"
        USDC = "USDC"
        STRK = "STRK"
        BTC = "BTC"
        ETH = "ETH"

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="payments")
    created_at = models.DateTimeField(
        auto_now_add=True, auto_created=True, db_index=True, null=False
    )
    updated_at = models.DateTimeField(
        auto_now_add=True, auto_created=True, db_index=True, null=False
    )
    expired_at = models.DateTimeField(db_index=True, null=False)
    network = models.CharField(
        max_length=20,
        choices=NetworkChoices.choices,
        default=NetworkChoices.Starknet,
        db_index=True,
        null=False,
    )

    currency = models.CharField(
        max_length=10,
        choices=CurrencyChoices.choices,
        default=CurrencyChoices.ETH,
        db_index=True,
        null=False,
    )
    value = models.DecimalField(
        max_digits=19, decimal_places=8, db_index=True, null=False
    )
    pay_wallet = models.CharField(max_length=150, null=False, db_index=True)
    state = models.CharField(
        max_length=10,
        choices=StateChoices.choices,
        default=StateChoices.OPEN,
        db_index=True,
    )
    external_order_id = models.CharField(max_length=100, null=False, db_index=True)
    external_order_title = models.CharField(max_length=100, null=False, db_index=True)
    external_order_desc = models.CharField(max_length=100, null=True, default="")
    external_image_url = models.CharField(max_length=200, null=True, default="")

    tx_hash = models.CharField(max_length=200, null=True, default="")

    paid_at = models.DateTimeField(db_index=True, null=True)
    paid_asset = models.CharField(
        max_length=10,
        choices=CurrencyChoices.choices,
        default=CurrencyChoices.ETH,
        db_index=True,
    )
    paid_amount = models.DecimalField(decimal_places=10, max_digits=20, null=True)
    paid_usd_rate = models.DecimalField(decimal_places=4, max_digits=10, null=True)

    fee_asset = models.CharField(
        max_length=10,
        choices=CurrencyChoices.choices,
        default=CurrencyChoices.ETH,
        db_index=True,
    )
    fee_amount = models.DecimalField(decimal_places=10, max_digits=20, null=True)

    net_asset = models.CharField(
        max_length=10,
        choices=CurrencyChoices.choices,
        default=CurrencyChoices.ETH,
        db_index=True,
    )
    net_amount = models.DecimalField(decimal_places=10, max_digits=20, null=True)

    metadata = models.JSONField(db_index=True, null=True)

    class Meta:
        db_table = "payments"
        verbose_name = "Payments"
        verbose_name_plural = "Payments"


class UserBalance(models.Model):
    updated_at = models.DateTimeField(
        auto_now_add=True, auto_created=True, db_index=True, null=False
    )
    network = models.CharField(
        max_length=20,
        choices=Payments.NetworkChoices.choices,
        default=Payments.NetworkChoices.Starknet,
        db_index=True,
        null=False,
    )
    currency = models.CharField(
        max_length=10,
        choices=Payments.CurrencyChoices.choices,
        default=Payments.CurrencyChoices.ETH,
        db_index=True,
        null=False,
    )
    value = models.DecimalField(
        max_digits=19, decimal_places=8, db_index=True, null=False, default=0
    )
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="balances")


class Transfer(models.Model):
    network = models.CharField(max_length=20, db_index=True)
    symbol = models.CharField(max_length=20, db_index=True)
    contract_address = models.CharField(max_length=100, db_index=True)
    block_hash = models.CharField(max_length=100, db_index=True)
    block_number = models.BigIntegerField(db_index=True)
    block_timestamp = models.DateTimeField(db_index=True)
    transaction_hash = models.CharField(max_length=150, db_index=True)
    transfer_id = models.CharField(max_length=150, db_index=True)
    from_address = models.CharField(max_length=150, db_index=True)
    to_address = models.CharField(max_length=150, db_index=True)
    amount = models.DecimalField(
        max_digits=50, decimal_places=18, db_index=True
    )  # Adjust max_digits and decimal_places as per your precision needs
    amount_raw = models.TextField()
    _cursor = (
        models.BigIntegerField()
    )  # Assuming '_cursor' field is for internal use, similar to 'id'

    class Meta:
        managed = False
        db_table = "transfers"  # Optional: Specify the database table name if different from the default (appname_modelname)
