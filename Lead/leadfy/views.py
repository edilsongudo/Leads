from .utils import *
from .forms import *
from .models import *
from django.forms.models import modelform_factory
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, FileResponse, JsonResponse
import json
import csv
import datetime
from django.forms import TextInput, EmailInput
from urllib.parse import urlparse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView
from django.urls import reverse
from ast import literal_eval as make_tuple
from django.db.models import Count
from django_pandas.io import read_frame
import folium
import pandas as pd



@login_required
def dashboard(request, days):
    day2 = datetime.date.today()
    day1 = day2 - datetime.timedelta(days=int(days))

    if request.is_ajax():
        if days == '0':
            return JsonResponse({'page_views': number_of_clicks(day1, day2, PageVisit, request), 'clicks_per_hours': hours(day1, day2, PageVisit, request)['hours'], 'labels': hours(day1, day2, PageVisit, request)['labels'], 'number_of_leads': number_of_leads(day1, day2, LeadModel, request)})
        elif days == '7':
            labels = get_days(day1, day2, PageVisit, request)['list_of_days2']
            return JsonResponse({'page_views': number_of_clicks(day1, day2, PageVisit, request), 'clicks_per_hours': get_days(day1, day2, PageVisit, request)['list_of_days'], 'labels': labels, 'number_of_leads': number_of_leads(day1, day2, LeadModel, request)})
        elif days == '30':
            labels = get_days(day1, day2, PageVisit, request)['list_of_days2']
            return JsonResponse({'page_views': number_of_clicks(day1, day2, PageVisit, request), 'clicks_per_hours': get_days(day1, day2, PageVisit, request)['list_of_days'], 'labels': labels, 'number_of_leads': number_of_leads(day1, day2, LeadModel, request)})

    return render(request, 'leadfy/dashboard.html')



def home(request):
    if request.user.is_authenticated:
        return redirect('landing_as_author_pv', username=request.user.username)
    else:
        return render(request, 'leadfy/home.html')

@login_required
def leads(request):
    response = HttpResponse(content_type="text/csv")
    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Date', 'Referrer', 'Refferer Main Domain', 'Location'])

    leads = LeadModel.objects.filter(lead_from=request.user)
    for lead in leads.values_list('name', 'email', 'date_submited', 'referer', 'referer_main_domain', 'location'):
        writer.writerow(lead)

    response['Content-Disposition'] = 'attachment; filename="Leads.csv"'

    return response



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
        response = redirect(link.link)
        form = CustomForm(data=request.POST)
        form.instance.lead_from = user
        form.instance.referer = set_http_referer(request, response, user.username)
        form.instance.referer_main_domain = urlparse(set_http_referer(request, response, user.username)).netloc
        form.instance.location = get_location(request)['country_name']
        form.instance.location_code = get_location(request)['country_code']
        if form.is_valid():
            form.save()
            response.set_cookie(f'{user.username}_captured', '', max_age=86400 * 365)
            return response

    if user.advanced.ask_visitors_to_subscribe_when_they_click_in_a_link == False:
        return redirect(link.link)

    if link.use_this_link_to_ask_visitors_to_subscribe == False:
        return redirect(link.link)

    if f'{user.username}_captured' in request.COOKIES:
        return redirect(link.link)

    context = context_dict(user=user, link=link, form=form)
    response = render(request, 'leadfy/emailcapture.html', context=context)

    set_http_referer(request, response, user.username)
    def save_statistics():
        link.view_count += 1
        link.save()
        new_visit = PageVisit(page=link)
        new_visit.referer = set_http_referer(request, response, user.username)
        new_visit.referer_main_domain = urlparse(set_http_referer(request, response, user.username)).netloc
        new_visit.location = get_location(request)['country_name']
        new_visit.location_code = get_location(request)['country_code']
        new_visit.save()

    if not user.username in request.COOKIES:
        max_age = user.advanced.seconds_to_wait_before_asking_user_to_subscribe_again
        response.set_cookie(user.username, '', max_age=max_age)
        if not short_url in request.COOKIES:
            response.set_cookie(short_url, short_url)
            save_statistics()
        return response
    else:
        save_statistics()
        return redirect(link.link)


def landing(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    links = Link.objects.filter(user=user).order_by('order')

    show_subscribe_button = True
    if f'{user.username}_captured' in request.COOKIES:
        show_subscribe_button = False

    context = context_dict(user=user, links=links, show_subscribe_button=show_subscribe_button)
    response = render(request, 'leadfy/landing.html', context=context)

    if not f'{user.username}_land' in request.COOKIES:
        response.set_cookie(f'{user.username}_land', '', max_age=86400 * 365)
        user.view_count += 1
        user.save()

    set_http_referer(request, response, user.username)
    return response


def stats(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    if user == request.user:
        links = Link.objects.filter(user=user).order_by('-view_count')

        allpagevisitsorderedbylocation = PageVisit.objects.values_list('location', 'location_code').annotate(truck_count=Count('location')).order_by('-truck_count')
        allpagevisitsorderedbyrefferer = PageVisit.objects.values_list('referer_main_domain').annotate(truck_count=Count('referer_main_domain')).order_by('-truck_count')
        df =  pd.DataFrame(allpagevisitsorderedbylocation, columns=['location', 'location_code', 'truck_count'])
        print(df)

        state_geo = 'custom.geo (1).json'
        m = folium.Map(location=[0, 0], zoom_start=1)
        folium.Choropleth(geo_data=state_geo, name='Choropleth', data=df, columns=['location', 'truck_count'], key_on="feature.properties.sovereignt", fill_color="YlGn", fill_opacity=0.7,
                          line_opacity=0.2, legend_name="Links Visits").add_to(m)
        folium.LayerControl().add_to(m)

        m = m._repr_html_()

        context = context_dict(user=user, links=links, m=m)
        response = render(request, 'leadfy/stats.html', context=context)
        return response
    else:
        return HttpResponseForbidden()

def landing_as_author_pv(request, username):
    user = get_object_or_404(get_user_model(), username=username)

    if request.is_ajax():
        data = json.loads(request.body)
        order = data['data']

        i = 1
        for short_url in order:
            link = Link.objects.get(short_url=short_url)
            link.order = i
            link.save()
            i += 1

    if request.user == user:
        links = Link.objects.filter(user=user).order_by('order')
        context = context_dict(user=user, links=links)
        response = render(request, 'leadfy/landing_as_author_pv.html', context=context)
        return response
    else:
        return HttpResponseForbidden()


def settings(request):
    response = render(request, 'leadfy/settings.html')
    return response


@login_required
def advanced(request):
    form = AdvancedForm(instance=request.user.advanced)
    if request.method == 'POST':
        form = AdvancedForm(request.POST, instance=request.user.advanced)
        if form.is_valid():
            form.save()
            return redirect('settings')
    context = context_dict(user=request.user, form=form)
    return render(request, 'leadfy/advanced.html', context)


@login_required
def preferences(request):
    form = PreferencesForm(instance=request.user.preferences)
    user = request.user

    if request.method == 'POST':
        preference = Preferences.objects.get(user=request.user)
        form = PreferencesForm(request.POST, request.FILES, instance=request.user.preferences)
        if form.is_valid():
            if request.POST['use_background_image'] == 'true':
                preference.use_background_image = True
            else:
                preference.use_background_image = False
            preference.font_family = request.POST['font']
            preference.color1 = request.POST['color1']
            preference.color2 = request.POST['color2']
            color1 = make_tuple(request.POST['color1'].replace('rgba', ''))
            color2 = make_tuple(request.POST['color2'].replace('rgba', ''))
            preference.body_font_color = contrast_gradient(color1, color2)
            preference.link_background_color = request.POST['link_background_color']
            # preference.link_text_color = request.POST['link_text_color']
            preference.link_text_color = contrast_color(make_tuple(request.POST['link_background_color'].replace('rgba', '')))
            alpha = make_tuple(request.POST['link_background_color'].replace('rgba', ''))[3]
            if int(alpha) <= 0.25:
                preference.link_border_color = "rgba(255, 255, 255, 1)"
            else:
                preference.link_border_color = request.POST['link_background_color']
            preference.primary_font_size = int(request.POST['primary_font_size'])
            preference.name_font_size = int(request.POST['name_font_size'])
            preference.background_image_brightness = int(request.POST['brightness'])
            preference.border_radius = int(request.POST['border_radius'])
            preference.save()
            return redirect('landing_as_author_pv', username=request.user.username)

    fonts = []
    for font in myfonts:
        fonts.append(font[0])
    links = Link.objects.filter(user=user)
    context = context_dict(user=user, form=form, fonts=fonts, links=links)
    return render(request, 'leadfy/preferences.html', context=context)



@login_required
def createlink(request):
    fields = '__all__'
    exclude = ['user', 'view_count', 'order']
    if request.user.subscription.plan == 'Free':
        exclude.append('short_url')
    widgets = {
        'title': TextInput(attrs={'placeholder': 'Link Title'}),
        'short_url': TextInput(attrs={'placeholder': 'Link short URL'}),
        'link': TextInput(attrs={'placeholder': 'Link Destionation URL'}),
    }
    CustomForm = modelform_factory(model=Link, fields=fields, widgets=widgets, exclude=exclude)
    form = CustomForm()
    # form = LinkCreateForm()
    if request.method == 'POST':
        # form = LinkCreateForm(request.POST)
        form = CustomForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            try:
                min_order = Link.objects.filter(user=request.user).order_by('order').first().order
            except: #There is not any link yet. This is the first one.
                min_order = 1
            form.instance.order = min_order - 1
            form.save()
            return redirect('landing_as_author_pv', username=request.user.username)
    context = context_dict(user=request.user, form=form)
    return render(request, 'leadfy/link-create.html', context)


@login_required
def editlink(request, short_url):
    link = get_object_or_404(Link, short_url=short_url)
    # form = LinkCreateForm(instance=link)
    fields = '__all__'
    exclude = ['user', 'view_count', 'short_url', 'order']
    widgets = {
        'title': TextInput(attrs={'placeholder': 'Link Title'}),
        'short_url': TextInput(attrs={'placeholder': 'Link short URL', 'disabled': 'disabled'}),
        'link': TextInput(attrs={'placeholder': 'Link Destionation URL'}),
    }
    CustomForm = modelform_factory(model=Link, fields=fields, widgets=widgets, exclude=exclude)
    form = CustomForm(instance=link)
    if request.user == link.user:
        if request.method == 'POST':
            # form = LinkCreateForm(request.POST, instance=link)
            form = CustomForm(request.POST, instance=link)
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                return redirect('landing_as_author_pv', username=request.user.username)
        context = context_dict(user=request.user, form=form, link=link)
        return render(request, 'leadfy/link-edit.html', context)
    else:
        return HttpResponseForbidden()



def deletelink(request, short_url):
    link = get_object_or_404(Link, short_url=short_url)
    if request.method == 'POST':
        link.delete()
        return redirect('landing_as_author_pv', username=request.user.username)
    context = context_dict(user=request.user, link=link)
    return render(request, 'leadfy/link_confirm_delete.html', context)


def error_404_view(request, exception):
    return render(request, 'leadfy/404.html')


@login_required
def desktopimage(request):
    preference = Preferences.objects.get(user=request.user)
    print('REQUEST RECEIVED', request.FILES.get('cropped'))
    preference.background_image_desktop = request.FILES.get('cropped')
    preference.save()
    return JsonResponse({'success': 'success'})

@login_required
def mobileimage(request):
    preference = Preferences.objects.get(user=request.user)
    print('REQUEST RECEIVED', request.FILES.get('cropped'))
    preference.background_image_mobile = request.FILES.get('cropped')
    preference.save()
    return JsonResponse({'success': 'success'})


@login_required
def socials(request):
    fields = '__all__'
    exclude = ['user']
    # widgets = {
    #     'instagram': TextInput(attrs={'placeholder': 'https://www.instagram.com/username'}),
    #     'facebook': TextInput(attrs={'placeholder': 'https://www.facebook.com/username'}),
    #     'youtube': TextInput(attrs={'placeholder': 'https://<channel link here>'}),
    # }
    CustomForm = modelform_factory(model=Social, fields=fields, exclude=exclude)
    form = CustomForm(instance=request.user.social)
    if request.method == 'POST':
        form = CustomForm(request.POST, instance=request.user.social)
        if form.is_valid():
            form.save()
            return redirect('settings')
    context = context_dict(user=request.user, form=form)
    return render(request, 'leadfy/socials.html', context)

@login_required
def integrations(request):
    fields = '__all__'
    exclude = ['user']
    widgets = {
        'facebook_pixel_id': TextInput(attrs={'placeholder': 'Facebook Pixel ID'}),
    }
    CustomForm = modelform_factory(model=Integrations, widgets=widgets, fields=fields, exclude=exclude)
    form = CustomForm(instance=request.user.integrations)
    if request.method == 'POST':
        form = CustomForm(request.POST, instance=request.user.social)
        if form.is_valid():
            form.save()
            return redirect('settings')
    context = context_dict(user=request.user, form=form)
    return render(request, 'leadfy/integrations.html', context)


def subscribe(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    fields = (['name', 'email'])
    widgets = {
        'name': TextInput(attrs={'placeholder': 'Name'}),
        'email': EmailInput(attrs={'placeholder': 'Email'})
    }
    CustomForm = modelform_factory(model=LeadModel, fields=fields, widgets=widgets)
    form = CustomForm()

    response = redirect('thankyou', username=username)

    if request.method == 'POST':
        form = CustomForm(data=request.POST)
        form.instance.lead_from = user
        form.instance.referer = set_http_referer(request, response, username)
        form.instance.referer_main_domain = urlparse(set_http_referer(request, response, user.username)).netloc
        form.instance.location = get_location(request)['country_name']
        form.instance.location_code = get_location(request)['country_code']
        if form.is_valid():
            form.save()
            response.set_cookie(f'{user.username}_captured', '', max_age=86400 * 365)
            return response

    context = context_dict(user=user, form=form)
    return render(request, 'leadfy/emailcapture.html', context=context)

def thankyou(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    context = context_dict(user=user)
    return render(request, 'leadfy/thankyou.html', context)
