# Generated by Django 3.0 on 2021-08-12 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leadfy', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='description',
        ),
    ]
