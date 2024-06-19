from django.contrib import admin
from django.contrib.admin import site
from django.urls import include, path
from django.views.generic.base import TemplateView

from allauth.account.decorators import secure_admin_login
from l2pay.l2pay.views import PaymentsView
from rest_framework import routers

admin.autodiscover()
admin.site.login = secure_admin_login(admin.site.login)


urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html")),
    path("accounts/", include("allauth.urls")),
    path("accounts/profile/", TemplateView.as_view(template_name="profile.html")),
    path("dashboard/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
]

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns += [
    # YOUR PATTERNS
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "schema/swagger-ui",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]


api_router = routers.DefaultRouter()
api_router.register(r"api/payments", PaymentsView)
urlpatterns += api_router.urls
