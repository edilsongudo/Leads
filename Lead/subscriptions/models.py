from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

plans = (
    ('Free', 'Free'),
    ('Premium', 'Premium')
)


class Subscription(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, null=True)
    plan = models.CharField(
        max_length=100, default="Free", choices=plans)
    paypal_subscription_id = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.plan}'
