# Generated by Django 3.0 on 2021-11-16 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadfy', '0050_auto_20211115_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='embed',
            name='youtube_video_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]