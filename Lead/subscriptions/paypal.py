import requests
import json
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from configparser import ConfigParser
import pprint

if settings.PAYPAL_ENV == 'sandbox':
    PAYPAL_BASE_ENDPOINT = 'api-m.sandbox'
elif settings.PAYPAL_ENV == 'live':
    PAYPAL_BASE_ENDPOINT = 'api-m'
else:
    print('CRITICAL ERROR, CHECK paypal.py line 14')

config = ConfigParser()
config.read('config.ini')

pp = pprint.PrettyPrinter(indent=1)

def get_access_token():

    now = timezone.now()
    now = now.strftime('%d-%b-%Y %H:%M:%S')
    now = datetime.strptime(now, '%d-%b-%Y %H:%M:%S')

    def get_token():
        print('PAYPAL ACCESS TOKEN HAS EXPIRED')
        h = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
        d = {'grant_type': 'client_credentials'}

        cid = settings.PAYPAL_CID
        secret = settings.PAYPAL_SECRET
        url = f'https://{PAYPAL_BASE_ENDPOINT}.paypal.com/v1/oauth2/token'

        r = requests.post(url, auth=(cid, secret), headers=h, data=d).json()

        access_token = r['access_token']
        expires_in = r['expires_in']
        expire_date = now + timedelta(seconds=expires_in)
        expire_date_string = expire_date.strftime('%d-%b-%Y %H:%M:%S')

        config.set(settings.PAYPAL_ENV, 'PAYPAL_ACCESS_TOKEN_EXPIRE_DATE', expire_date_string)
        config.set(settings.PAYPAL_ENV, 'access_token', access_token)
        with open('config.ini', 'w') as f:
            config.write(f)
        return access_token

    #GET ACCESS TOKEN IF DOES NOT EXIST
    access_token = config[settings.PAYPAL_ENV]['access_token']
    token_expire_date = config[settings.PAYPAL_ENV]['PAYPAL_ACCESS_TOKEN_EXPIRE_DATE']
    if token_expire_date == '' or access_token == '':
        access_token = get_token()

    access_token = config[settings.PAYPAL_ENV]['access_token']
    token_expire_date = config[settings.PAYPAL_ENV]['PAYPAL_ACCESS_TOKEN_EXPIRE_DATE']
    token_expire_date = datetime.strptime(token_expire_date, '%d-%b-%Y %H:%M:%S')

    if now > token_expire_date:
        access_token = get_token()
        return access_token

    print('PAYPAL ACCESS TOKEN HAS NOT EXPIRED')
    return access_token


def create_product(access_token, product_name='Links Service', description='Links Service', product_type='SERVICE',
                   category='SOFTWARE', product_name_id=None):
    h = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
        # 'PayPal-Request-Id': ''
    }

    d = {
        'name': product_name,
        'description': description,
        'type': product_type,
        'category': category,
        # 'image_url': 'https://example.com/streaming.jpg',
        # 'home_url': 'https://example.com/home'
    }

    url = f'https://{PAYPAL_BASE_ENDPOINT}.paypal.com/v1/catalogs/products'
    response = requests.post(url, headers=h, json=d).json()
    return response


def create_plan(access_token, product_id, name='Premium Plan', description='Premium Plan',
                frequency='MONTH', price=6, tenure='REGULAR', sequence=1, total_cycles=0,
                auto_billing=True, setup_fee=0, setup_fee_failure_action='CONTINUE', payment_failure_threshold=3):

    url = f'https://{PAYPAL_BASE_ENDPOINT}.paypal.com/v1/billing/plans'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        # 'Paypal-Request-Id': name_id,
    }

    data = {
        'product_id': product_id,
        'name': name,
        'description': description,
        'billing_cycles': [
            {
                'frequency': {
                    'interval_unit': frequency,
                    'interval_count': 1,
                },
                'pricing_scheme': {
                    'fixed_price': {
                        'currency_code': 'USD',
                        'value': price
                    }
                },
                'tenure_type': tenure,
                'sequence': sequence,
                'total_cycles': total_cycles,
            }
        ],
        'payment_preferences': {
            'auto_bill_outstanding': auto_billing,
            'setup_fee': {
                'currency_code': 'USD',
                'value': setup_fee
            },
            'setup_fee_failure_action': setup_fee_failure_action,
            'payment_failure_threshold': payment_failure_threshold
        },
        'taxes': {
            'percentage': '0',
            'inclusive': True,
        }
    }

    response = requests.post(url, headers=headers, json=data).json()
    return response


def get_subscription_details(access_token, subID):
    h = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    url = f'https://{PAYPAL_BASE_ENDPOINT}.paypal.com/v1/billing/subscriptions/{subID}'
    r = requests.get(url, headers=h).json()
    return r


def activate_subscription(access_token, subID):
    h = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    d = {"reason": "Reactivating subscription"}
    d = json.dumps(d)

    url = f'https://{PAYPAL_BASE_ENDPOINT}.paypal.com/v1/billing/subscriptions/{subID}/activate'
    r = requests.post(url, headers=h, data=d)
    return r


def cancel_subscription(access_token, subID):
    h = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    url = f'https://{PAYPAL_BASE_ENDPOINT}.paypal.com/v1/billing/subscriptions/{subID}/cancel'
    r = requests.post(url, headers=h)
    return r


def suspend_subscription(access_token, subID):
    h = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    d = {"reason": "Costumer Suspended subscription"}
    d = json.dumps(d)

    url = f'https://{PAYPAL_BASE_ENDPOINT}.paypal.com/v1/billing/subscriptions/{subID}/suspend'
    r = requests.post(url, headers=h)
    return r


def list_products(access_token):

    h = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    url = f'https://{PAYPAL_BASE_ENDPOINT}.paypal.com/v1/catalogs/products?page_size=2&page=1&total_required=true'
    r = requests.get(url, headers=h).json()
    return r


def list_plans(access_token):

    h = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    url = f'https://{PAYPAL_BASE_ENDPOINT}.paypal.com/v1/billing/plans?page_size=10&page=1&total_required=true'
    r = requests.get(url, headers=h).json()
    return r


def plans_details(access_token, plan_id):

    h = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    url = f'https://{PAYPAL_BASE_ENDPOINT}.paypal.com/v1/billing/plans/{plan_id}'
    r = requests.get(url, headers=h).json()
    return r

# print(get_access_token())
# pp.pprint(plans_details(get_access_token(), settings.PAYPAL_PLAN_ID))
# pp.pprint(create_plan(get_access_token(), config[settings.PAYPAL_ENV]['product_id']))
