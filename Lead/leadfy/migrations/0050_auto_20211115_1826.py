# Generated by Django 3.0 on 2021-11-15 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadfy', '0049_auto_20211115_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='embed',
            name='youtube_video_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
