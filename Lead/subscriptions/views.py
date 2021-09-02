from django.shortcuts import render
from .models import Subscription
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .paypal import *
from .utils import *
from datetime import datetime
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.conf import settings


@login_required
def subscribe(request):
    PAYPAL_PLAN_ID = settings.PAYPAL_PLAN_ID
    if request.user.subscription.plan == 'Free':
        return render(request, 'subscriptions/codingnepal.html', {'plan_id': PAYPAL_PLAN_ID})
    else:
        return HttpResponseForbidden()


@login_required
def activate(request, subID):
    activate_subscription(request.user, subID)
    return render(request, 'subscriptions/activate.html')


@login_required
def deactivate(request, subID):
    return render(request, 'subscriptions/deactivate.html')


@login_required
def manage_subs(request):
    manage_subscriptions()
    return JsonResponse({'Success': 'Success'})
