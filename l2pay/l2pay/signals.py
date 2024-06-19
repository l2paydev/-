import logging
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import Group
from django.db.models.signals import post_save

from l2pay.l2pay.models import Payments

logger = logging.getLogger(__name__)


@receiver(user_signed_up)
def handle_user_signed_up(sender, request, user, **kwargs):
    user.is_staff = True  # or False
    user.save()
    merchant = Group.objects.get(name="merchant")
    user.groups.add(merchant)