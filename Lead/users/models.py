from django.db import models
# from django.contrib.auth.models import User
from PIL import Image

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = models.TextField(blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    name = models.CharField(max_length=30, default="")
    bio = models.CharField(max_length=200, default="", blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        if self.name == "":
            self.name = self.user.username
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
