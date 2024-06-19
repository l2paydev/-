import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from drf_spectacular.utils import extend_schema
from rest_framework import status

from l2pay.l2pay.models import MerchantKey, Payments
from l2pay.l2pay.serializer import (
    PaymentsSerializer,
    CreatePaymentSerializer,
    RetrievePaymentsSerializer,
)

from .permissions import HasMerchantKey

# Create your views here.

# from rest_framework_api_key.authentication


class PaymentsView(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [HasMerchantKey]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return PaymentsSerializer
        elif self.action in ["create"]:
            return CreatePaymentSerializer
        return PaymentsSerializer  # Default to list serializer for other actions

    def get_permissions(self):
        # super().get_permissions()
        if self.action in ["list", "create"]:
            return [HasMerchantKey()]
        return [permissions.AllowAny()]

    @extend_schema(
        description="Get a payment",
        summary="Get a payment",
        responses=RetrievePaymentsSerializer,
        auth=[],
        # Add additional schema configurations if needed
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        scheme = request.META.get("HTTP_X_FORWARDED_PROTO", "http")
        host = request.META.get("HTTP_HOST", "localhost:3000")
        data["pay_url"] = f"{scheme}://{host}/payments/{instance.id}"
        return Response(data)

    @extend_schema(
        description="List payments",
        summary="List payments",
        responses=PaymentsSerializer,
        auth=[{"Merchant": []}],
        # Add additional schema configurations if needed
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description="Create a payment",
        summary="Create a payment",
        responses=RetrievePaymentsSerializer,
        auth=[{"Merchant": []}],
        # Add additional schema configurations if needed
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        data = RetrievePaymentsSerializer(instance=instance).data
        scheme = request.META.get("HTTP_X_FORWARDED_PROTO", "http")
        host = request.META.get("HTTP_HOST", "localhost:3000")
        data["pay_url"] = f"{scheme}://{host}/payments/{instance.id}"
        headers = self.get_success_headers(serializer.data)
        return Response(
            data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
