from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Preferences, Advanced, Social, Integrations
from .writecss import writecss


@receiver(post_save, sender=get_user_model())
def create_Preferences(sender, instance, created, **kwargs):
    if created:
        Preferences.objects.create(user=instance)
        Advanced.objects.create(user=instance)
        Social.objects.create(user=instance)
        Integrations.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_Preferences(sender, instance, created, **kwargs):
    instance.preferences.save()
    instance.advanced.save()
    instance.social.save()
    instance.integrations.save()


@receiver(post_save, sender=Preferences)
def save_Preferences(sender, instance, created, **kwargs):
    writecss(instance.user)
