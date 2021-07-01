from django.db import models
from django.contrib.auth.models import User
from .utils import generate_ref_code


class LeadModel(models.Model):
    name = models.CharField(max_length=100, null=True, blank=False)
    email = models.EmailField(null=True, blank=False)
    lead_from = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.email


class Preferences(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=12, blank=True, null=True)
    link = models.URLField(
        max_length=200, default='http://www.yourlink.com', null=True, blank=False)
    button_text = models.CharField(max_length=20, null=True,
                                   default='Download', blank=False)
    bio = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} preferences'

    def save(self, *args, **kwargs):
        if self.code == '' or self.code == None:
            code = generate_ref_code()
            self.code = code

        if self.bio == '' or self.bio == None:
            self.bio = 'Would you like to give your email, so I can share things you may find interesting?'

        super().save(*args, **kwargs)
