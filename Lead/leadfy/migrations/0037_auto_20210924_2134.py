# Generated by Django 3.0 on 2021-09-24 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadfy', '0036_auto_20210923_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='social',
            name='discord',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='social',
            name='github',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='social',
            name='messenger',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='social',
            name='skype',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='social',
            name='twitch',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='font_family',
            field=models.CharField(choices=[['aAffirmation.otf', 'aAffirmation.otf'], ['aAlwaysSmile.otf', 'aAlwaysSmile.otf'], ['AmaticSC-Regular.ttf', 'AmaticSC-Regular.ttf'], ['CirrusWisp.otf', 'CirrusWisp.otf'], ['Juliagar.otf', 'Juliagar.otf'], ['Karla-VariableFont_wght.ttf', 'Karla-VariableFont_wght.ttf'], ['No Virus.otf', 'No Virus.otf']], default='Juliagar.otf', max_length=100, null=True),
        ),
    ]
