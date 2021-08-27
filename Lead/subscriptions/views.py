from django.shortcuts import render
from .models import Subscription
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .paypal import *
from .utils import *
from datetime import datetime
from django.http import HttpResponse, HttpResponseForbidden


@login_required
def subscribe(request):
    if request.user.subscription.plan == 'Free':
        return render(request, 'subscriptions/subscribe.html')
    else:
        return HttpResponseForbidden()

# BE CAREFUL DO NOT ALLOW USERS USE A FAKE PAYPAL ID


@login_required
def activate(request, subID):
    activate_subscription(request.user, subID)
    return render(request, 'subscriptions/activate.html')


@login_required
def deactivate(request, subID):
    return render(request, 'subscriptions/deactivate.html')
