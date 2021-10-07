from django.db import models
from django.contrib.auth import get_user_model
from .utils import generate_ref_code, generate_netloc
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
import os
from PIL import Image
from django_resized import ResizedImageField


class LeadModel(models.Model):
    name = models.CharField(max_length=100, null=True, blank=False)
    email = models.EmailField(null=True, blank=False)
    lead_from = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, blank=True)
    date_submited = models.DateTimeField(default=timezone.now)
    referer = models.CharField(max_length=200, null=True, blank=True)
    referer_main_domain = models.CharField(
        max_length=200, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    location_code = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.email


class Link(models.Model):
    short_url = models.SlugField(
        default=generate_ref_code,
        null=True,
        unique=True)
    title = models.CharField(max_length=20, null=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True)
    link = models.URLField(
        max_length=200, null=True, blank=False)
    show_link = models.BooleanField(default=True)
    use_this_link_to_ask_visitors_to_subscribe = models.BooleanField(
        default=False)
    view_count = models.PositiveIntegerField(
        default=0)
    order = models.IntegerField(
        default=1)

    def __str__(self):
        return f'{self.short_url}'

    def save(self, *args, **kwargs):
        # if not self.netloc:
        #     self.netloc = generate_netloc(self.link)
        self.short_url = self.short_url.lower()
        super(Link, self).save(*args, **kwargs)


# class TrackCode(models.Model):
#     code = models.CharField(max_length=100, null=True, blank=True)
#     title = models.CharField(max_length=100, null=True, blank=True)
#     description models.CharField(max_length=100, null=True, blank=True)


# class SiteVisit(models.Model):
#     track_code = models.ForeignKey(TrackCode, on_delete=models.CASCADE, null=True, blank=True)
#     time = models.DateTimeField(default=timezone.now)
#     referer = models.CharField(max_length=200, null=True, blank=True)
#     referer_main_domain = models.CharField(
#         max_length=200, null=True, blank=True)
#     location = models.CharField(max_length=100, null=True, blank=True)
#     location_code = models.CharField(max_length=100, null=True, blank=True)
#     device_type = models.CharField(max_length=100, null=True, blank=True)
#     os_type = models.CharField(max_length=100, null=True, blank=True)


class PageVisit(models.Model):
    page = models.ForeignKey(
        Link, on_delete=models.CASCADE, null=True)
    time = models.DateTimeField(default=timezone.now)
    referer = models.CharField(max_length=200, null=True, blank=True)
    referer_main_domain = models.CharField(
        max_length=200, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    location_code = models.CharField(max_length=100, null=True, blank=True)
    device_type = models.CharField(max_length=100, null=True, blank=True)
    os_type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'/{self.page.short_url} at {self.time}'


fonts_folder = os.path.join(settings.MEDIA_ROOT, 'fonts')
fonts = os.listdir(fonts_folder)
myfonts = []
for font in fonts:
    if font.split('.')[-1] in ('otf', 'ttf'):
        myfonts.append([font, font])


class Preferences(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, null=True)
    color1 = models.CharField(
        max_length=100, default="rgba(130.517, 189.457, 212.85, 1)")
    color2 = models.CharField(
        max_length=100, default="rgba(151.462, 111.687, 143.872, 1)")
    body_font_color = models.CharField(
        max_length=100, default="rgba(255, 255, 255, 1)")
    background_image_desktop = models.ImageField(
        upload_to='usersbackgroundimages',
        default="usersbackgroundimages/defaultdesktopbackgroundimage.jpg",
        null=True)
    background_image_mobile = models.ImageField(
        upload_to='usersbackgroundimages',
        default="usersbackgroundimages/defaultmobilebackgroundimage.jpg",
        null=True)
    background_image_brightness = models.IntegerField(
        default=50, validators=[MinValueValidator(0), MaxValueValidator(100)])
    use_background_image = models.BooleanField(default=False)
    font_family = models.CharField(
        max_length=100, null=True, default="Karla-VariableFont_wght.ttf", choices=myfonts)
    primary_font_size = models.PositiveIntegerField(
        default=16, validators=[MinValueValidator(0), MaxValueValidator(100)])
    name_font_size = models.PositiveIntegerField(
        default=16, validators=[MinValueValidator(0), MaxValueValidator(100)])
    border_radius = models.PositiveIntegerField(
        default=50, validators=[MinValueValidator(0), MaxValueValidator(50)])
    link_background_color = models.CharField(
        max_length=100, default="rgba(255, 255, 255, 1)")
    link_border_color = models.CharField(
        max_length=100, default="rgba(255, 255, 255, 1)")
    link_text_color = models.CharField(
        max_length=100, default="rgba(0, 0, 0, 1)")
    lastmodified = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self.user.username} Landing Page Preferences'

    def save(self, *args, **kwargs):
        super(Preferences, self).save(*args, **kwargs)


class Advanced(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    seconds_to_wait_before_asking_user_to_subscribe_again = models.PositiveIntegerField(
        default=3600, validators=[MinValueValidator(0), MaxValueValidator(324000)])
    # ask_visitors_to_subscribe_when_they_click_in_a_link = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} Advanced Preferences'


class SubscribeButton(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    call_to_action = models.CharField(
        max_length=150,
        default="Would you like to subscribe to my email list?")
    call_to_action_button_text = models.CharField(
        max_length=20, default="Subscribe")
    show = models.BooleanField(default=True)
    # view_count = models.IntegerField(
    #     default=0)

    def __str__(self):
        return f'{self.user.username} Advanced Preferences'


class Social(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, null=True)
    instagram = models.URLField(
        max_length=200, null=True, blank=True)
    facebook = models.URLField(
        max_length=200, null=True, blank=True)
    tiktok = models.URLField(
        max_length=200, null=True, blank=True)
    youtube = models.URLField(
        max_length=200, null=True, blank=True)
    twitter = models.URLField(
        max_length=200, null=True, blank=True)
    spotify = models.URLField(
        max_length=200, null=True, blank=True)
    pinterest = models.URLField(
        max_length=200, null=True, blank=True)
    whatsapp = models.URLField(
        max_length=200, null=True, blank=True)
    linkedin = models.URLField(
        max_length=200, null=True, blank=True)
    snapchat = models.URLField(
        max_length=200, null=True, blank=True)
    telegram = models.URLField(
        max_length=200, null=True, blank=True)
    github = models.URLField(
        max_length=200, null=True, blank=True)
    twitch = models.URLField(
        max_length=200, null=True, blank=True)
    discord = models.URLField(
        max_length=200, null=True, blank=True)
    skype = models.URLField(
        max_length=200, null=True, blank=True)
    email = models.EmailField(
        max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}'


class Integrations(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, null=True)
    facebook_pixel_id = models.CharField(
        max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}'
