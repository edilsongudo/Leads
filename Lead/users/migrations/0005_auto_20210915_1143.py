# Generated by Django 3.0 on 2021-09-15 09:43

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210915_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, default='default.jpg', force_format='JPEG', keep_meta=True, quality=30, size=[100, 100], upload_to='profile_pics'),
        ),
    ]