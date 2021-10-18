from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Subscription


@receiver(post_save, sender=get_user_model())
def create_Preferences(sender, instance, created, **kwargs):
    if created and not kwargs.get('raw', False):
        Subscription.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_Preferences(sender, instance, created, **kwargs):
    if not kwargs.get('raw', False):
        instance.subscription.save()
