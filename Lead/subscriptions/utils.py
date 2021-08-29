from .paypal import *
from django.conf import settings
from .paypal import get_access_token
from .models import Subscription


def activate_subscription(user, SubID):
    details = get_subscription_details(
        get_access_token(), SubID)
    status = details['status']
    outstanding_amt = float(
        details['billing_info']['outstanding_balance']['value'])
    outstanding_amt = int(outstanding_amt)

    if outstanding_amt <= 0 and status == 'ACTIVE':
        sub = Subscription.objects.get(user=user)
        sub.plan = 'Premium'
        sub.paypal_subscription_id = SubID
        sub.save()


def downgrade_subscription(user):
    details = get_subscription_details(
        get_access_token(), user.subscription.paypal_subscription_id)
    status = details['status']
    outstanding_amt = float(
        details['billing_info']['outstanding_balance']['value'])
    outstanding_amt = int(outstanding_amt)

    sub = Subscription.objects.get(user=user)

    if outstanding_amt >= 40:
        sub.plan = 'Free'
        sub.save()
        # Send an user telling user that his account has been deactivated due to payment issues
