# Generated by Django 3.0 on 2021-09-15 09:43

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('leadfy', '0034_auto_20210915_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preferences',
            name='background_image_desktop',
            field=django_resized.forms.ResizedImageField(crop=None, default='usersbackgroundimages/defaultdesktopbackgroundimage.jpg', force_format='JPEG', keep_meta=True, null=True, quality=30, size=[1280, 720], upload_to='usersbackgroundimages'),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='background_image_mobile',
            field=django_resized.forms.ResizedImageField(crop=None, default='usersbackgroundimages/defaultmobilebackgroundimage.jpg', force_format='JPEG', keep_meta=True, null=True, quality=30, size=[720, 1280], upload_to='usersbackgroundimages'),
        ),
    ]