from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from allauth.account.signals import user_signed_up


class L2PAYConfig(AppConfig):
    name = "l2pay.l2pay"
    # verbose_name = _("L2PAY")
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        try:
            from . import signals

            user_signed_up.connect(signals.handle_user_signed_up)

            print("Signals imported successfully.")
        except ImportError as e:
            print(f"Error importing signals: {e}")
