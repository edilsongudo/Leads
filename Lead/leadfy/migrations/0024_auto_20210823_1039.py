# Generated by Django 3.0 on 2021-08-23 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadfy', '0023_auto_20210822_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preferences',
            name='link_border_color',
            field=models.CharField(default='rgba(0, 0, 0, 1)', max_length=100),
        ),
    ]
