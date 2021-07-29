# Generated by Django 3.0 on 2021-07-28 19:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadfy', '0006_preferences_name_font_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='preferences',
            name='border_radius',
            field=models.IntegerField(default=48, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50)]),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='name_font_size',
            field=models.IntegerField(default=48, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='primary_font_size',
            field=models.IntegerField(default=16, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
