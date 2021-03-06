# Generated by Django 3.0 on 2021-11-16 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadfy', '0051_embed_youtube_video_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='embed',
            old_name='youtube_video_id',
            new_name='youtube_video_id_1',
        ),
        migrations.RemoveField(
            model_name='embed',
            name='youtube_video_url',
        ),
        migrations.AddField(
            model_name='embed',
            name='title_1',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='embed',
            name='title_2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='embed',
            name='title_3',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='embed',
            name='youtube_video_id_2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='embed',
            name='youtube_video_id_3',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='embed',
            name='youtube_video_url_1',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='embed',
            name='youtube_video_url_2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='embed',
            name='youtube_video_url_3',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
