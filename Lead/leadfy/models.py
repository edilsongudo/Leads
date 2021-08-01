from django.db import models
from django.contrib.auth import get_user_model
from .utils import generate_ref_code
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class LeadModel(models.Model):
    name = models.CharField(max_length=100, null=True, blank=False)
    email = models.EmailField(null=True, blank=False)
    lead_from = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True)
    date_submited = models.DateTimeField(default=timezone.now)
    referer = models.CharField(max_length=200, null=True, blank=True)
    referer_main_domain = models.CharField(
        max_length=200, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.email


class Link(models.Model):
    title = models.CharField(max_length=30, null=True, default='My Website')
    description = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True)
    short_url = models.SlugField(default=generate_ref_code, null=True)
    link = models.URLField(
        max_length=200, default='http://www.google.com', null=True, blank=False)
    view_count = models.IntegerField(
        default=0)

    def __str__(self):
        return f'{self.short_url}'


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


myfonts = (
    ('Gloss_And_Bloom.ttf', 'Gloss_And_Bloom.ttf'),
    ('Heaters.otf', 'Heaters.otf'),
    ('Arial.ttf', 'Arial.ttf'),
)


class Preferences(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, null=True)
    color1 = models.CharField(
        max_length=100, default="#E8CBC0")
    color2 = models.CharField(
        max_length=100,  default="#636FA4")
    background_image_desktop = models.ImageField(
        upload_to='usersbackgroundimages', default="defaultdesktopbackgroundimage.jpg", null=True)
    background_image_mobile = models.ImageField(
        upload_to='usersbackgroundimages', default="defaultmobilebackgroundimage.jpg", null=True)
    background_image_brightness = models.IntegerField(
        default=50, validators=[MinValueValidator(0), MaxValueValidator(100)])
    use_background_image = models.BooleanField(default=False)
    font_family = models.CharField(
        max_length=100, null=True, default="Heaters.otf", choices=myfonts)
    primary_font_size = models.IntegerField(
        default=25, validators=[MinValueValidator(0), MaxValueValidator(100)])
    name_font_size = models.IntegerField(
        default=25, validators=[MinValueValidator(0), MaxValueValidator(100)])
    border_radius = models.IntegerField(
        default=50, validators=[MinValueValidator(0), MaxValueValidator(50)])
    link_background_color = models.CharField(
        max_length=100,  default="#ffffff")
    link_text_color = models.CharField(
        max_length=100,  default="#000000")

    def __str__(self):
        return f'{self.user.username} Landing Page Preferences'
