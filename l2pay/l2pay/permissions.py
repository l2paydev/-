from typing import Any
from django.http import HttpRequest
from rest_framework_api_key.permissions import BaseHasAPIKey
from .models import MerchantKey


class HasMerchantKey(BaseHasAPIKey):
    model = MerchantKey

    def has_permission(self, request: HttpRequest, view: Any) -> bool:
        valid = super().has_permission(request, view)
        if valid:
            key = request.META["HTTP_AUTHORIZATION"].split()[1]
            api_key = MerchantKey.objects.get_from_key(key)
            request.api_key = api_key
            request.api_key_user = api_key.user
            request.user = api_key.user
        return valid
