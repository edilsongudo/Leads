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
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    image = ResizedImageField(
        default='default.jpg', size=[300, 300], force_format='JPEG', upload_to='profile_pics')
    name = models.CharField(max_length=30, default="")
    bio = models.CharField(
        max_length=200, default="Hello, here you can see some of my favorite links", blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        if self.name == "":
            self.name = self.user.username
        super(Profile, self).save(*args, **kwargs)

        # img = Image.open(self.image.path)

        # if img.height > 100 or img.width > 100:
        #     output_size = (100, 100)
        #     img.thumbnail(output_size)
        #     img.save(self.image.path, quality=30)
