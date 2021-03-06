# Generated by Django 3.0 on 2021-08-10 18:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(choices=[('Free', 'Free'), ('Premium', 'Premium')], default='Free', max_length=100)),
                ('paypal_subscription_id', models.CharField(max_length=30, null=True)),
                ('paypal_subscription_status', models.CharField(max_length=30, null=True)),
                ('paid_until', models.DateTimeField(null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
