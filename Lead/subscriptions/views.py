from django.shortcuts import render


def subscribe(request):
    return render(request, 'subscriptions/subscribe.html')


def activate(request, subID):
    print(subID)
    return render(request, 'subscriptions/activate.html')


def deactivate(request, subID):
    print(subID)
    return render(request, 'subscriptions/deactivate.html')
