from django.db import models
from django.contrib.auth import get_user_model
from .utils import generate_ref_code, generate_netloc
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
import os


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

    def __str__(self):
        return self.email


class Link(models.Model):
    show_link = models.BooleanField(default=True)
    title = models.CharField(max_length=30, null=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True)
    short_url = models.SlugField(default=generate_ref_code, null=True, unique=True)
    link = models.URLField(
        max_length=200, null=True, blank=False)
    view_count = models.IntegerField(
        default=0)

    def __str__(self):
        return f'{self.short_url}'

    # def save(self, *args, **kwargs):
    #     if not self.netloc:
    #         self.netloc = generate_netloc(self.link)
    #         super(Link, self).save(*args, **kwargs)


class PageVisit(models.Model):
    page = models.ForeignKey(
        Link, on_delete=models.CASCADE, null=True)
    time = models.DateTimeField(default=timezone.now)
    referer = models.CharField(max_length=200, null=True, blank=True)
    referer_main_domain = models.CharField(
        max_length=200, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)

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
        max_length=100, default="#9B23FA")
    color2 = models.CharField(
        max_length=100,  default="#8AFBD8")
    body_font_color = models.CharField(
        max_length=100,  default="rgb(255, 255, 255)")
    background_image_desktop = models.ImageField(
        upload_to='usersbackgroundimages', default="usersbackgroundimages/defaultdesktopbackgroundimage.jpg", null=True)
    background_image_mobile = models.ImageField(
        upload_to='usersbackgroundimages', default="usersbackgroundimages/defaultmobilebackgroundimage.jpg", null=True)
    background_image_brightness = models.IntegerField(
        default=50, validators=[MinValueValidator(0), MaxValueValidator(100)])
    use_background_image = models.BooleanField(default=False)
    font_family = models.CharField(
        max_length=100, null=True, default="arial.ttf", choices=myfonts)
    primary_font_size = models.IntegerField(
        default=16, validators=[MinValueValidator(0), MaxValueValidator(100)])
    name_font_size = models.IntegerField(
        default=16, validators=[MinValueValidator(0), MaxValueValidator(100)])
    border_radius = models.IntegerField(
        default=10, validators=[MinValueValidator(0), MaxValueValidator(50)])
    link_background_color = models.CharField(
        max_length=100,  default="#000000")
    link_text_color = models.CharField(
        max_length=100,  default="#ffffff")

    def __str__(self):
        return f'{self.user.username} Landing Page Preferences'


class Advanced(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    ask_visitors_to_subscribe = models.BooleanField(default=False)
    call_to_action = models.CharField(max_length=150, default="Before you go please, would you like to subscribe to my email list? Hint: You can skip this step if you wish.")
    call_to_action_button_text = models.CharField(max_length=20, default="Subscribe")
    seconds_to_wait_before_asking_user_to_subscribe_again = models.IntegerField(
        default=3600, validators=[MinValueValidator(0), MaxValueValidator(324000)])

    def __str__(self):
        return f'{self.user.username} Advanced Preferences'
