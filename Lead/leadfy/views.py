from .forms import *
from .models import *
from django.forms.models import modelform_factory
# from django.contrib.auth.models import User
from users.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
import json
from django.http import FileResponse, JsonResponse
import datetime
from .utils import get_geo
from django.forms import TextInput, EmailInput
from urllib.parse import urlparse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView
from django.urls import reverse

from .views_utils import *


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard', days='0')
    else:
        return render(request, 'leadfy/home.html')

@login_required
def leads(request):
    leads = LeadModel.objects.filter(lead_from=request.user)
    return render(request, 'leadfy/leads.html', {'leads': leads})


def lead(request, short_url):
    link = get_object_or_404(Link, short_url=short_url)
    user = link.user

    fields = (['name', 'email'])
    widgets = {
        'name': TextInput(attrs={'placeholder': 'Name'}),
        'email': EmailInput(attrs={'placeholder': 'Email'})
    }
    CustomForm = modelform_factory(model=LeadModel, fields=fields, widgets=widgets)
    form = CustomForm()
    if request.method == 'POST':
        if 'skip' in request.POST:
            return redirect(link.link)
        form = CustomForm(data=request.POST)
        form.instance.lead_from = user
        form.instance.referer = set_http_referer(request)
        form.instance.referer_main_domain = urlparse(set_http_referer(request)).netloc
        form.instance.location = get_location(request)
        if form.is_valid():
            form.save()
            return redirect(link.link)

    context = context_dict(user=user, link=link, form=form)
    response = render(request, 'leadfy/emailcapture.html', context=context)

    set_http_referer(request, response=response)
    def save_statistics():
        link.view_count += 1
        link.save()
        new_visit = PageVisit(page=link)
        new_visit.referer = set_http_referer(request, response=response)
        new_visit.referer_main_domain = urlparse(set_http_referer(request, response=response)).netloc
        new_visit.location = get_location(request)
        new_visit.save()

    if not 'tried_to_capture_email' in request.COOKIES:
        response.set_cookie('tried_to_capture_email', '', max_age=30)
        if not short_url in request.COOKIES:
            response.set_cookie(short_url, short_url)
            save_statistics()
        return response
    else:
        save_statistics()
        return redirect(link.link)


def landing(request, username):
    user = get_object_or_404(User, username=username)
    links = Link.objects.filter(user=user)
    context = context_dict(user=user, links=links)
    response = render(request, 'leadfy/landing.html', context=context)
    set_http_referer(request, response=response)
    return response

def landing_as_author_pv(request, username):
    user = get_object_or_404(User, username=username)

    if request.user == user:
        links = Link.objects.filter(user=user)
        context = context_dict(user=user, links=links)
        response = render(request, 'leadfy/landing_as_author_pv.html', context=context)
        return response
    else:
        return HttpResponseForbidden()



@login_required
def preferences(request):
    form = PreferencesForm(instance=request.user.preferences)
    user = request.user

    if request.method == 'POST':
        form = PreferencesForm(request.POST, request.FILES, instance=request.user.preferences)
        if form.is_valid():
            form.instance.color1 = request.POST['color1']
            form.instance.color2 = request.POST['color2']
            form.instance.link_background_color = request.POST['link_background_color']
            form.instance.link_text_color = request.POST['link_text_color']
            form.instance.primary_font_size = request.POST['primary_font_size']
            form.instance.name_font_size = request.POST['name_font_size']
            form.instance.background_image_brightness = request.POST['brightness']
            form.instance.border_radius = request.POST['border_radius']
            form.save()
            return redirect('preferences')
    context = context_dict(user=user, form=form)
    return render(request, 'leadfy/preferences.html', context=context)



@login_required
def createlink(request):
    form = LinkCreateForm()
    if request.method == 'POST':
        form = LinkCreateForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('landing_as_author_pv', username=request.user.username)
    return render(request, 'leadfy/link-create.html', {'form': form})


@login_required
def editlink(request, short_url):
    link = get_object_or_404(Link, short_url=short_url)
    form = LinkCreateForm(instance=link)
    if request.user == link.user:
        if request.method == 'POST':
            form = LinkCreateForm(request.POST, instance=link)
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                return redirect('landing_as_author_pv', username=request.user.username)
        return render(request, 'leadfy/link-edit.html', {'form': form, 'link': link})
    else:
        return HttpResponseForbidden()


class LinkDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Link

    def get_success_url(self):
        return reverse('landing_as_author_pv', kwargs={'username': self.request.user.username})

    def test_func(self):
        link = self.get_object()
        if self.request.user == link.user:
            return True
        return False


def error_404_view(request, exception):
    return render(request, 'leadfy/404.html')


@login_required
def dashboard(request, days):
    day2 = datetime.date.today()
    day1 = day2 - datetime.timedelta(days=int(days))

    def get_days(date1, date2):
        delta = day2 - day1
        list_of_days = []
        list_of_days2 = []
        for i in range(delta.days + 1):
            day = day1 + datetime.timedelta(days=i)
            pages_visits = PageVisit.objects.filter(
                page__user=request.user, time__date=day).count()
            list_of_days.append(pages_visits)
            list_of_days2.append(f'{day.strftime("%d/%m")}')
        return {'list_of_days': list_of_days, 'list_of_days2': list_of_days2}

    def number_of_clicks(date1, date2):
        number_of_clicks = PageVisit.objects.filter(
            page__user=request.user, time__date__gte=date1, time__date__lte=date2).count()
        return number_of_clicks

    def number_of_leads(date1, date2):
        number_of_leads = LeadModel.objects.filter(lead_from=request.user, date_submited__date__gte=date1, date_submited__date__lte=date2).count()
        return number_of_leads

    def hours(date1, date2):
        hours = []
        labels = []
        for i in range(0, 24):
            pages_visits = PageVisit.objects.filter(
                page__user=request.user, time__date__gte=date1, time__date__lte=date2, time__hour=i)
            hours.append(len(pages_visits))
            labels.append(i)
        return {'hours': hours, 'labels': labels}

    if request.is_ajax():
        if days == '0':
            return JsonResponse({'page_views': number_of_clicks(day1, day2), 'clicks_per_hours': hours(day1, day2)['hours'], 'labels': hours(day1, day2)['labels'], 'number_of_leads': number_of_leads(day1, day2)})
        elif days == '7':
            labels = get_days(day1, day2)['list_of_days2']
            return JsonResponse({'page_views': number_of_clicks(day1, day2), 'clicks_per_hours': get_days(day1, day2)['list_of_days'], 'labels': labels, 'number_of_leads': number_of_leads(day1, day2)})
        elif days == '30':
            labels = get_days(day1, day2)['list_of_days2']
            return JsonResponse({'page_views': number_of_clicks(day1, day2), 'clicks_per_hours': get_days(day1, day2)['list_of_days'], 'labels': labels, 'number_of_leads': number_of_leads(day1, day2)})

    return render(request, 'leadfy/dashboard.html')
