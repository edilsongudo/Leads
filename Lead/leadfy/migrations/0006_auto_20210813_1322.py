# Generated by Django 3.0 on 2021-08-13 11:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadfy', '0005_link_show_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='netloc',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='show_link',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='background_image_desktop',
            field=models.ImageField(default='usersbackgroundimages/defaultdesktopbackgroundimage.jpg', null=True, upload_to='usersbackgroundimages'),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='background_image_mobile',
            field=models.ImageField(default='usersbackgroundimages/defaultmobilebackgroundimage.jpg', null=True, upload_to='usersbackgroundimages'),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='name_font_size',
            field=models.IntegerField(default=16, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='primary_font_size',
            field=models.IntegerField(default=16, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
