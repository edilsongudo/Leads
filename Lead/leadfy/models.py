from django.db import models
from django.contrib.auth.models import User
from .utils import generate_ref_code
from django.utils import timezone


class LeadModel(models.Model):
    name = models.CharField(max_length=100, null=True, blank=False)
    email = models.EmailField(null=True, blank=False)
    lead_from = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    date_submited = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email


class Page(models.Model):
    title = models.CharField(max_length=30, null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    code = models.SlugField(blank=True, null=True)
    link = models.URLField(
        max_length=200, default='http://www.yourdestinationurl.com', null=True, blank=False)
    button_text = models.CharField(max_length=20, null=True,
                                   default='Your cta', blank=False)
    bio = models.CharField(max_length=200, null=True,
                           default='Tell your users about what you have to offer them here', blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    view_count = models.IntegerField(
        default=0)

    def __str__(self):
        return f'{self.code}'

    def save(self, *args, **kwargs):
        if self.code == '' or self.code == None:
            code = generate_ref_code()
            self.code = code

        super().save(*args, **kwargs)


class PageVisit(models.Model):
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, null=True)
    time = models.DateTimeField(default=timezone.now)
    country = models.CharField(max_length=50, null=True, blank=True)
    referer = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'/{self.page.code} at {self.time}'
