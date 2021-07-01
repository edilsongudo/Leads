from .forms import PreferencesForm
from .models import LeadModel
from django.forms.models import modelform_factory
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return render(request, 'leadfy/dash.html')
    return render(request, 'leadfy/home.html')


@login_required
def preferences(request):
    form = PreferencesForm(instance=request.user.preferences)
    if request.method == 'POST':
        form = PreferencesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'leadfy/preferences.html', {'form': form})


def lead(request, username):
    user = get_object_or_404(User, username=username)
    fields = (['name', 'email'])
    CustomForm = modelform_factory(model=LeadModel, fields=fields)
    form = CustomForm()
    if request.method == 'POST':
        form = CustomForm(data=request.POST)
        form.instance.lead_from = user
        if form.is_valid():
            form.save()
            return redirect(request.user.preferences.link)
    return render(request, 'leadfy/lead.html', {'form': form, 'user': user})


def error_404_view(request, exception):
    return render(request, 'leadfy/404.html')
