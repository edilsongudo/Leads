# Generated by Django 3.0 on 2021-11-17 19:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import leadfy.storage


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leadfy', '0054_preferences_css_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preferences',
            name='css_file',
        ),
        migrations.CreateModel(
            name='CustomCss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('css_file', models.FileField(blank=True, null=True, storage=leadfy.storage.OverwriteStorage(), upload_to='customstylesheets')),
                ('lastmodified', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
