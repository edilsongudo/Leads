# Generated by Django 3.0 on 2021-11-17 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadfy', '0053_auto_20211116_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='preferences',
            name='css_file',
            field=models.FileField(blank=True, null=True, upload_to='cssfiles'),
        ),
    ]
