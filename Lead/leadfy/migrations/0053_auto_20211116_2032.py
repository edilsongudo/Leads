# Generated by Django 3.0 on 2021-11-16 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadfy', '0052_auto_20211116_2006'),
    ]

    operations = [
        migrations.RenameField(
            model_name='embed',
            old_name='youtube_video_id_1',
            new_name='youtube_video_id',
        ),
        migrations.RenameField(
            model_name='embed',
            old_name='youtube_video_url_1',
            new_name='youtube_video_url',
        ),
        migrations.RemoveField(
            model_name='embed',
            name='title_1',
        ),
        migrations.RemoveField(
            model_name='embed',
            name='title_2',
        ),
        migrations.RemoveField(
            model_name='embed',
            name='title_3',
        ),
        migrations.RemoveField(
            model_name='embed',
            name='youtube_video_id_2',
        ),
        migrations.RemoveField(
            model_name='embed',
            name='youtube_video_id_3',
        ),
        migrations.RemoveField(
            model_name='embed',
            name='youtube_video_url_2',
        ),
        migrations.RemoveField(
            model_name='embed',
            name='youtube_video_url_3',
        ),
        migrations.AddField(
            model_name='embed',
            name='title',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
