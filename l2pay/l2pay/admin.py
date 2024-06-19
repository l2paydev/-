import os
import secrets
from typing import Tuple
from django import forms
from django.contrib import admin
from django.db.models.base import Model as Model
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html
from rest_framework_api_key.models import AbstractAPIKey, APIKey
from .models import Payments, Settings, MerchantKey, UserBalance
from rest_framework_api_key.admin import APIKeyModelAdmin, APIKeyAdmin

from snowflake import SnowflakeGenerator

mid = os.getenv("MachineID", 0)
snowflakeIdGen = SnowflakeGenerator(mid)


@admin.register(Settings)
class SettingAdmin(admin.ModelAdmin):
    list_display = (
        "webhook_url",
        "payout_address",
        "updated_at",
    )

    readonly_fields = (
        "user",
        "updated_at",
    )

    def save_model(
        self,
        request: HttpRequest,
        obj: AbstractAPIKey,
        form: None,
        change: bool = False,
    ) -> None:
        obj.user = request.user
        return super().save_model(request, obj, form, change)

    def get_list_display(self, request: HttpRequest):
        if request.user.is_superuser:
            return super().get_list_display(request) + ("user",)
        return super().get_list_display(request)

    def get_queryset(self, request):
        # Get the original queryset
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)
        # Filter the queryset to include only records that belong to the current user
        return queryset

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return not super().get_queryset(request).filter(user=request.user).exists()


@admin.register(MerchantKey)
class MerchantKeyAdmin(APIKeyModelAdmin):
    list_display = [*APIKeyModelAdmin.list_display, "user"]

    search_fields = [*APIKeyModelAdmin.search_fields, "user"]

    def get_readonly_fields(
        self, request: HttpRequest, obj: Model = None
    ) -> Tuple[str, ...]:
        return super().get_readonly_fields(request, obj) + ("user",)

    def save_model(
        self,
        request: HttpRequest,
        obj: AbstractAPIKey,
        form: None,
        change: bool = False,
    ) -> None:
        obj.user = request.user
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        # Get the original queryset
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)
        # Filter the queryset to include only records that belong to the current user
        return queryset


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in Payments._meta.get_fields()
        if field.name
        not in [
            "user",
        ]
    ]

    def get_queryset(self, request):
        # Get the original queryset
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)
        # Filter the queryset to include only records that belong to the current user
        return queryset

    def get_list_display(self, request: HttpRequest):
        if request.user.is_superuser:
            return super().get_list_display(request) + [
                "user",
            ]
        return super().get_list_display(request)


@admin.register(UserBalance)
class UserBalanceAdmin(admin.ModelAdmin):
    list_display = (
        "network",
        "currency",
        "value",
        "updated_at",
    )

    def get_list_display(self, request: HttpRequest):
        result = super().get_list_display(request)
        if request.user.is_superuser:
            result = result + ("user",)
        return result

    def get_queryset(self, request):
        # Get the original queryset
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)
        # Filter the queryset to include only records that belong to the current user
        return queryset


admin.site.unregister(APIKey)
