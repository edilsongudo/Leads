# Generated by Django 3.0 on 2021-10-06 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadfy', '0040_auto_20211006_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='social',
            name='email',
            field=models.EmailField(blank=True, max_length=200, null=True),
        ),
    ]
