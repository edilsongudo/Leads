# Generated by Django 3.0 on 2021-08-11 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_remove_subscription_paid_until'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='paypal_subscription_status',
        ),
    ]