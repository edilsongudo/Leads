# Generated by Django 3.0 on 2021-07-21 15:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leadfy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preferences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('background_color_1', models.CharField(max_length=100, null=True)),
                ('background_color_2', models.CharField(max_length=100, null=True)),
                ('background_image', models.ImageField(null=True, upload_to='usersbackgroundimages')),
                ('font_family', models.CharField(choices=[('Gloss_And_Bloom.ttf', 'Gloss_And_Bloom.ttf'), ('Heaters.otf', 'Heaters.otf')], max_length=100, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
