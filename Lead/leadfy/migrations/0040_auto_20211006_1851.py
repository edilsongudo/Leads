# Generated by Django 3.0 on 2021-10-06 16:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadfy', '0039_auto_20210926_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advanced',
            name='seconds_to_wait_before_asking_user_to_subscribe_again',
            field=models.PositiveIntegerField(default=3600, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(324000)]),
        ),
        migrations.AlterField(
            model_name='link',
            name='view_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='border_radius',
            field=models.PositiveIntegerField(default=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50)]),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='name_font_size',
            field=models.PositiveIntegerField(default=16, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='primary_font_size',
            field=models.PositiveIntegerField(default=16, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
