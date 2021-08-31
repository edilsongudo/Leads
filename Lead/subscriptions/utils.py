from .paypal import *
from django.conf import settings
from .paypal import get_access_token
from .models import Subscription
import pprint
from datetime import datetime, timedelta


pp = pprint.PrettyPrinter(indent=1)


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


# def downgrade_subscription(subscription):
#     details = get_subscription_details(
#         get_access_token(), subscription.paypal_subscription_id)

#     next_billing_time = False
#     status = details['status']
#     if status != 'ACTIVE':
#         try:
#             next_billing_time = details['billing_info']['next_billing_time']
#             next_billing_time = next_billing_time.split('T')[0]
#             next_billing_time = datetime.strptime(
#                 next_billing_time, '%Y-%m-%d')
#             print(next_billing_time, type(next_billing_time))
#         except KeyError:
#             return 'Free'
#         except Exception as e:
#             print(e)
#             return 'Premium'

#     if next_billing_time:
#         if next_billing_time < datetime.now():
#             print('Downgrading Account')
#             return 'Free'
#     # pp.pprint(details)
#     print('Account remains Premium')
#     return 'Premium'


# def manage_subscriptions():
#     subscriptions = Subscription.objects.filter(plan='Premium')
#     for subscription in subscriptions:
#         plan = downgrade_subscription(subscription)
#         print(plan)
#         # subscription.plan = plan
