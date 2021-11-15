from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Preferences, Advanced, SubscribeButton, Social, Integrations, Link, Embed
from .writecss import writecss
from .utils import generate_ref_code


@receiver(post_save, sender=get_user_model())
def create_Preferences(sender, instance, created, **kwargs):
    if created and not kwargs.get('raw', False):
        Preferences.objects.create(user=instance)
        Advanced.objects.create(user=instance)
        Social.objects.create(user=instance)
        Integrations.objects.create(user=instance)
        SubscribeButton.objects.create(user=instance)
        Embed.objects.create(user=instance)
        # Link.objects.create(short_url=generate_ref_code(),
        #                     title='demo', user=instance, show_link=False)


@receiver(post_save, sender=get_user_model())
def save_Preferences(sender, instance, created, **kwargs):
    if not kwargs.get('raw', False):
        instance.preferences.save()
        instance.advanced.save()
        instance.subscribebutton.save()
        instance.social.save()
        instance.integrations.save()
        instance.embed.save()


@receiver(post_save, sender=Preferences)
def save_Preferences(sender, instance, created, **kwargs):
    writecss(instance.user)
