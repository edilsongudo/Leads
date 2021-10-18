from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image
from django_resized import ResizedImageField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    view_count = models.IntegerField(
        default=0)


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, null=True)
    first_time_login = models.BooleanField(default=False)
    image = models.ImageField(
        default='default.jpg',
        upload_to='profile_pics')
    name = models.CharField(max_length=30, default="")
    bio = models.CharField(
        max_length=200,
        default="Hello, here you can see some of my favorite links",
        blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        if self.name == "":
            self.name = self.user.username
        super(Profile, self).save(*args, **kwargs)
