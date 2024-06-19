from datetime import datetime, timedelta
from rest_framework import serializers
from .models import Payments
from .util import gen_account_address


class PaymentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        exclude = ["user"]


class RetrievePaymentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        exclude = ["user"]

    pay_url = serializers.CharField(max_length=200, required=False)


class CreatePaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        fields = [
            "network",
            "currency",
            "value",
            "external_order_id",
            "external_order_title",
            "external_order_desc",
            "external_image_url",
        ]

    value = serializers.DecimalField(max_digits=19, decimal_places=8)
    external_order_desc = serializers.CharField(max_length=100, required=False)
    external_image_url = serializers.CharField(max_length=200, required=False)

    def create(self, validated_data):
        user = self.context["request"].user
        # Get the current UTC datetime
        utc_now = datetime.utcnow()
        # Add 15 minutes to the current UTC datetime
        expired_at = utc_now + timedelta(minutes=15)
        validated_data["expired_at"] = expired_at
        validated_data["user"] = user
        validated_data["pay_wallet"] = gen_account_address()
        instance = super().create(validated_data)
        return instance
