# Generated by Django 3.0 on 2021-09-24 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leadfy', '0037_auto_20210924_2134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='social',
            name='messenger',
        ),
    ]
