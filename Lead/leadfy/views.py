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
def profile(request):
    return render(request, 'leadfy/profile.html')


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
            return redirect('home')
    return render(request, 'leadfy/lead.html', {'form': form})


def error_404_view(request, exception):
    return render(request, 'leadfy/404.html')
