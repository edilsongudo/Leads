from .utils import *
from .forms import *
from .models import *
from django.contrib import messages
from django.forms.models import modelform_factory
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import (
    HttpResponse, HttpResponseForbidden,
    FileResponse, JsonResponse)
import json
import csv
import datetime
from django.utils import timezone
from django.forms import TextInput, EmailInput
from urllib.parse import urlparse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView
from django.urls import reverse
from ast import literal_eval as make_tuple
from django.db.models import Count
from django_pandas.io import read_frame
import plotly.express as px
import plotly.io as pio
from django.utils.decorators import decorator_from_middleware
from django.db import IntegrityError
from django.contrib.auth.decorators import user_passes_test
from .custom_middleware import SimpleMiddleWare


@login_required
def choose_template(request):
    if request.method == 'POST':
        if request.is_ajax:
            data = json.loads(request.body)
            print(data)
            request.user.preferences.template = data['template']
            request.user.preferences.save()
    templates = Template.objects.all()
    return render(request, 'leadfy/choose_template.html', {'templates': templates})


@login_required
def dashboard(request, days):
    if request.user.subscription.plan == 'Free':
        return redirect('subscribe')
    day2 = datetime.date.today()
    day1 = day2 - datetime.timedelta(days=int(days))

    channels = get_referers(day1, day2, PageVisit, request)['channels']
    visits = get_referers(day1, day2, PageVisit, request)['visits']

    if request.is_ajax():
        if days == '0':
            return JsonResponse(
                {

                    'page_views': number_of_clicks(
                        day1,
                        day2,
                        PageVisit,
                        request),
                    'channels': channels,
                    'visits': visits,
                    'clicks_per_hours': hours(
                        day1,
                        day2,
                        PageVisit,
                        request)['hours'],
                    'labels': hours(
                        day1,
                        day2,
                        PageVisit,
                        request)['labels'],
                    'number_of_leads': number_of_leads(
                        day1,
                        day2,
                        LeadModel,
                        request)
                }
            )

        elif days == '7':
            labels = get_days(day1, day2, PageVisit, request)['list_of_days2']
            return JsonResponse(
                {
                    'page_views': number_of_clicks(
                        day1,
                        day2,
                        PageVisit,
                        request),
                    'channels': channels,
                    'visits': visits,
                    'clicks_per_hours': get_days(
                        day1,
                        day2,
                        PageVisit,
                        request)['list_of_days'],
                    'labels': labels,
                    'number_of_leads': number_of_leads(
                        day1,
                        day2,
                        LeadModel,
                        request)})

        elif days == '30':
            labels = get_days(day1, day2, PageVisit, request)['list_of_days2']
            return JsonResponse(
                {
                    'page_views': number_of_clicks(
                        day1,
                        day2,
                        PageVisit,
                        request),
                    'channels': channels,
                    'visits': visits,
                    'clicks_per_hours': get_days(
                        day1,
                        day2,
                        PageVisit,
                        request)['list_of_days'],
                    'labels': labels,
                    'number_of_leads': number_of_leads(
                        day1,
                        day2,
                        LeadModel,
                        request)})

    m = get_map(day1, day2, PageVisit, request)

    # data = {
    #     'id': ['Mozambique', 'Brazil', 'Portugal', 'Argentina'],
    #     'country_code': ['Mozambique', 'Brazil', 'Portugal', 'Argentina'],
    #     'visits': [80, 128, 4, 100]
    # }

    # df = pd.DataFrame(data)
    # df.set_index('country_code', inplace=True)
    # print(df)

    # state_geo = json.load(open('geoip/custom.geo (1).json', 'r'))

    # for feature in state_geo['features']:
    #     feature['id'] = feature['properties']['sovereignt']

    # m = px.choropleth(df, locations="id",
    #                   geojson=state_geo, color="visits")
    # # m.show()
    # m = m.to_html()

    return render(request, 'leadfy/dashboard.html', {'m': m})

def home(request):
    if request.user.is_authenticated:
        if not request.user.profile.first_time_login:
            request.user.profile.first_time_login = True
            request.user.profile.save()
            return redirect('profile')
        return redirect('landing_as_author_pv', username=request.user.username)
    else:
        return render(request, 'leadfy/revo.html')


@login_required
def exportleads(request):
    # if request.user.subscription.plan == 'Free':
    #     return redirect('subscribe')

    response = HttpResponse(content_type="text/csv")
    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Referrer',
                    'Location', 'Date'])

    leads = LeadModel.objects.filter(lead_from=request.user)
    for lead in leads.values_list(
        'name',
        'email',
        'referer_main_domain',
        'location',
        'date_submited'):
        lead = list(lead)
        time = lead[-1]
        time = datetime.datetime.strftime(time, '%d-%m-%Y')
        lead[-1] = time
        writer.writerow(lead)

    now = timezone.now()
    now = datetime.datetime.strftime(now, '%d-%m-%Y %H %M %S')
    filename = f'attachment; filename="Leads.csv {now}"'
    response['Content-Disposition'] = filename

    return response


@login_required
def exportlinks(request):
    if request.user.subscription.plan == 'Free':
        return redirect('subscribe')

    response = HttpResponse(content_type="text/csv")
    writer = csv.writer(response)
    writer.writerow(['Link', 'Referrer',
                    'Location', 'Device', 'OS', 'time'])

    visits = PageVisit.objects.filter(page__user=request.user)
    for visit in visits.values_list(
        'page__title',
        'referer_main_domain',
        'location',
        'device_type',
        'os_type',
        'time'):
        visit = list(visit)
        time = visit[-1]
        time = datetime.datetime.strftime(time, '%d-%m-%Y %H:%M:%S')
        visit[-1] = time
        writer.writerow(visit)

    now = timezone.now()
    now = datetime.datetime.strftime(now, '%d-%m-%Y %H %M %S')
    filename = f'attachment; filename="IndividualVisits {now}.csv"'
    response['Content-Disposition'] = filename

    return response


@login_required
def exportlink(request, short_url):
    if request.user.subscription.plan == 'Free':
        return redirect('subscribe')

    response = HttpResponse(content_type="text/csv")
    writer = csv.writer(response)
    writer.writerow(['Referrer',
                     'Location',
                     'Device',
                     'OS',
                     'time'])

    visits = PageVisit.objects.filter(page__short_url=short_url)
    for visit in visits.values_list(
        'referer_main_domain',
        'location',
        'device_type',
        'os_type',
        'time'):
        visit = list(visit)
        time = visit[-1]
        time = datetime.datetime.strftime(time, '%d-%m-%Y %H:%M:%S')
        visit[-1] = time
        writer.writerow(visit)

    now = timezone.now()
    now = datetime.datetime.strftime(now, '%d-%m-%Y %H %M %S')
    filename = f'attachment; filename="{short_url} visits {now}.csv"'
    response['Content-Disposition'] = filename

    return response

@decorator_from_middleware(SimpleMiddleWare)
def lead(request, short_url):
    link = get_object_or_404(Link, short_url__iexact=short_url)
    user = link.user

    fields = (['name', 'email'])
    widgets = {
        'name': TextInput(attrs={'placeholder': 'Name'}),
        'email': EmailInput(attrs={'placeholder': 'Email'})
    }
    CustomForm = modelform_factory(
        model=LeadModel,
        fields=fields,
        widgets=widgets)
    form = CustomForm()
    if request.method == 'POST':
        if 'skip' in request.POST:
            return redirect(link.link)
        response = redirect(link.link)
        form = CustomForm(data=request.POST)
        form.instance.lead_from = user
        form.instance.referer = set_http_referer(
            request, response, user.username)
        form.instance.referer_main_domain = urlparse(
            set_http_referer(request, response, user.username)).netloc
        form.instance.location = get_location(request)['country_name']
        form.instance.location_code = get_location(request)['country_code']
        if form.is_valid():
            form.save()
            response.set_cookie(
                f'{user.username}_captured',
                '',
                max_age=86400 * 365)
            return response

    context = context_dict(user=user, link=link, form=form)

    def save_statistics(response):
        set_http_referer(request, response, user.username)

        if user.username not in request.COOKIES:
            max_age = user.advanced.seconds_to_wait_before_asking_user_to_subscribe_again
            response.set_cookie(user.username, '', max_age=max_age)

        if short_url not in request.COOKIES:
            response.set_cookie(short_url, short_url)
            link.view_count += 1
            link.save()
            new_visit = PageVisit(page=link)
            new_visit.referer = set_http_referer(
                request, response, user.username)
            new_visit.referer_main_domain = urlparse(
                set_http_referer(request, response, user.username)).netloc
            new_visit.location = get_location(request)['country_name']
            new_visit.location_code = get_location(request)['country_code']
            new_visit.device_type = get_user_agent(request)['device_type']
            new_visit.os_type = get_user_agent(request)['os_type']
            new_visit.save()
        return response

    response = render(request, 'leadfy/emailcapture.html', context=context)
    if not link.use_this_link_to_ask_visitors_to_subscribe:
        response = redirect(link.link)

    if f'{user.username}_captured' in request.COOKIES:
        response = redirect(link.link)

    # if short_url in request.COOKIES:
    #     response = redirect(link.link)

    if user.username in request.COOKIES:
        response = redirect(link.link)

    return save_statistics(response)


def landing(request, username):
    user = get_object_or_404(get_user_model(), username__iexact=username)
    links = Link.objects.filter(user=user).order_by('order')

    show_subscribe_button = True
    if f'{user.username}_captured' in request.COOKIES:
        show_subscribe_button = False

    context = context_dict(
        user=user,
        links=links,
        show_subscribe_button=show_subscribe_button)
    response = render(request, 'leadfy/landing.html', context=context)

    if f'{user.username}_land' not in request.COOKIES:
        response.set_cookie(f'{user.username}_land', '', max_age=86400 * 365)
        user.view_count += 1
        user.save()

    set_http_referer(request, response, user.username)
    return response

@login_required
def stats(request, username):

    user = get_object_or_404(get_user_model(), username=username)
    if user == request.user:
        links = Link.objects.filter(user=user).order_by('-view_count')
        context = context_dict(user=user, links=links)
        response = render(request, 'leadfy/stats.html', context=context)
        return response
    else:
        raise PermissionDenied()


@login_required
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
        response = render(
            request,
            'leadfy/landing_as_author_pv.html',
            context=context)
        return response
    else:
        raise PermissionDenied()


@login_required
def settings(request):
    response = render(request, 'leadfy/settings.html')
    return response


@login_required
def export(request):
    response = render(request, 'leadfy/export.html')
    return response


@login_required
def advanced(request):
    # if request.user.subscription.plan == 'Free':
    #     return redirect('subscribe')

    form = AdvancedForm(instance=request.user.advanced)
    if request.method == 'POST':
        form = AdvancedForm(request.POST, instance=request.user.advanced)
        if form.is_valid():
            form.save()
            # return redirect('settings')
            return redirect(
                'user-landing',
                username=request.user.username)
    context = context_dict(user=request.user, form=form)
    return render(request, 'leadfy/advanced.html', context)


@login_required
def subscribebutton(request):
    form = SubscribeButtonForm(instance=request.user.subscribebutton)
    if request.method == 'POST':
        form = SubscribeButtonForm(
            request.POST, instance=request.user.subscribebutton)
        if form.is_valid():
            form.save()
            return redirect(
                'subscribe',
                username=request.user.username)
    context = context_dict(user=request.user, form=form)
    return render(request, 'leadfy/subscribebutton.html', context)


@login_required
def embed(request):
    form = EmbedForm(instance=request.user.embed)
    if request.method == 'POST':
        form = EmbedForm(
            request.POST, instance=request.user.embed)
        if form.is_valid():
            form.save()
            return redirect(
                'user-landing',
                username=request.user.username)
    context = context_dict(user=request.user, form=form)
    return render(request, 'leadfy/embed.html', context)


@login_required
def preferences(request):
    form = PreferencesForm(instance=request.user.preferences)
    user = request.user

    if request.method == 'POST':
        preference = Preferences.objects.get(user=request.user)
        form = PreferencesForm(
            request.POST,
            request.FILES,
            instance=request.user.preferences)
        if form.is_valid():
            preference.template = 'custom'
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
            preference.link_text_color = contrast_color(make_tuple(
                request.POST['link_background_color'].replace('rgba', '')))
            alpha = make_tuple(
                request.POST['link_background_color'].replace(
                    'rgba', ''))[3]
            if int(alpha) <= 0.25:
                preference.link_border_color = "rgba(255, 255, 255, 1)"
            else:
                preference.link_border_color = request.POST['link_background_color']
            preference.primary_font_size = int(
                request.POST['primary_font_size'])
            # int(request.POST['name_font_size'])
            preference.name_font_size = int(request.POST['primary_font_size'])
            preference.background_image_brightness = int(
                request.POST['brightness'])
            preference.border_radius = int(request.POST['border_radius'])
            preference.save()
            return redirect(
                'user-landing',
                username=request.user.username)

    fonts = []
    for font in myfonts:
        fonts.append(font[0])
    links = Link.objects.filter(user=user)
    context = context_dict(user=user, form=form, fonts=fonts, links=links)
    return render(request, 'leadfy/preferences.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def create_template(request):

    if request.method == 'POST':

        color1 = make_tuple(request.POST['color1'].replace('rgba', ''))
        color2 = make_tuple(request.POST['color2'].replace('rgba', ''))
        body_font_color = contrast_gradient(color1, color2)

        alpha = make_tuple(
            request.POST['link_background_color'].replace(
                'rgba', ''))[3]
        if int(alpha) <= 0.25:
            link_border_color = "rgba(255, 255, 255, 1)"
        else:
            link_border_color = request.POST['link_background_color']

        if request.POST['use_background_image'] == 'true':
            use_background_image = True
        else:
            use_background_image = False

        template = Template.objects.create(
            name=request.POST['name'],
            color1=request.POST['color1'],
            color2=request.POST['color2'],
            body_font_color=contrast_gradient(color1, color2),
            font_family=request.POST['font'],
            link_background_color=request.POST['link_background_color'],
            link_text_color = contrast_color(make_tuple(
                            request.POST['link_background_color'].replace('rgba', ''))),
            border_radius=int(request.POST['border_radius']),
            primary_font_size = int(
                            request.POST['primary_font_size']),
            link_border_color=link_border_color,
            use_background_image=use_background_image
        )

        return redirect('preferences')

    fonts = []
    for font in myfonts:
        fonts.append(font[0])

    User = get_user_model()
    user = User.objects.first()
    links = Link.objects.filter(user=user)
    context = context_dict(user=user, fonts=fonts, links=links)
    return render(request, 'leadfy/createtemplate.html', context=context)


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

    labels = {
        'short_url': 'selflink.link/to/'
    }

    help_texts = {
        'use_this_link_to_ask_visitors_to_subscribe': '''Whether to ask visitors
        to subscribe or not when they click this link''',
        'show_link': '''Whether to show or hide this link from your bio page.
        Note: Link will still be accessible outside your page'''
    }

    CustomForm = modelform_factory(
        model=Link,
        fields=fields,
        widgets=widgets,
        exclude=exclude,
        labels=labels,
        help_texts=help_texts)
    form = CustomForm()
    # form = LinkCreateForm()
    if request.method == 'POST':
        # form = LinkCreateForm(request.POST)

        form = CustomForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            try:
                min_order = Link.objects.filter(
                    user=request.user).order_by('order').first().order
            except BaseException:  # There is not any link yet. This is the first one.
                min_order = 1
                form.instance.order = min_order - 1

            try:
                form.save()
            except IntegrityError as e:
                messages.error(request, f'Link with slug "{form.instance.short_url}" already exists')
                context = context_dict(user=request.user, form=form)
                return render(request, 'leadfy/link-create.html', context)

            return redirect(
                'link-edit',
                short_url=form.instance.short_url)
    context = context_dict(user=request.user, form=form)
    return render(request, 'leadfy/link-create.html', context)


@login_required
def editlink(request, short_url):
    link = get_object_or_404(Link, short_url=short_url)
    # form = LinkCreateForm(instance=link)
    fields = '__all__'
    exclude = ['user', 'view_count', 'link', 'short_url', 'order']
    widgets = {
        'title': TextInput(attrs={'placeholder': 'Link Title'}),
        'short_url': TextInput(attrs={'placeholder': 'Link short URL', 'disabled': 'disabled'}),
        # 'link': TextInput(attrs={'placeholder': 'Link Destionation URL', 'disabled': 'disabled'}),
    }

    help_texts = {
        'use_this_link_to_ask_visitors_to_subscribe': '''Whether to ask visitors
        to subscribe or not when they click this link''',
        'show_link': '''Whether to show or hide this link from your bio page.
        Note: Link will still be accessible outside your page'''
    }

    CustomForm = modelform_factory(
        model=Link,
        fields=fields,
        widgets=widgets,
        exclude=exclude,
        help_texts=help_texts)
    form = CustomForm(instance=link)
    if request.user == link.user:
        if request.method == 'POST':
            # form = LinkCreateForm(request.POST, instance=link)
            form = CustomForm(request.POST, instance=link)
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                return redirect(
                    'user-landing',
                    username=request.user.username)
        context = context_dict(user=request.user, form=form, link=link)
        return render(request, 'leadfy/link-edit.html', context)
    else:
        raise PermissionDenied()

@login_required
def deletelink(request, short_url):
    link = get_object_or_404(Link, short_url=short_url)
    if request.user == link.user:
        if request.method == 'POST':
            link.delete()
            return redirect('landing_as_author_pv', username=request.user.username)
        context = context_dict(user=request.user, link=link)
        return render(request, 'leadfy/link_confirm_delete.html', context)
    else:
        raise PermissionDenied()



@login_required
def socials(request):
    # if request.user.subscription.plan == 'Free':
    #     return redirect('subscribe')
    fields = '__all__'
    exclude = ['user']
    # widgets = {
    #     'instagram': TextInput(attrs={'placeholder': 'https://www.instagram.com/username'}),
    #     'facebook': TextInput(attrs={'placeholder': 'https://www.facebook.com/username'}),
    #     'youtube': TextInput(attrs={'placeholder': 'https://<channel link here>'}),
    # }
    CustomForm = modelform_factory(
        model=Social, fields=fields, exclude=exclude)
    form = CustomForm(instance=request.user.social)
    if request.method == 'POST':
        form = CustomForm(request.POST, instance=request.user.social)
        if form.is_valid():
            form.save()
            # return redirect('settings')
            return redirect(
                'user-landing',
                username=request.user.username)
    context = context_dict(user=request.user, form=form)
    return render(request, 'leadfy/socials.html', context)


@login_required
def integrations(request):
    if request.user.subscription.plan == 'Free':
        return redirect('subscribe')
    fields = '__all__'
    exclude = ['user']
    widgets = {'facebook_pixel_id': TextInput(
        attrs={'placeholder': 'Facebook Pixel ID'}), }
    CustomForm = modelform_factory(
        model=Integrations,
        widgets=widgets,
        fields=fields,
        exclude=exclude)
    form = CustomForm(instance=request.user.integrations)
    if request.method == 'POST':
        form = CustomForm(request.POST, instance=request.user.social)
        if form.is_valid():
            form.save()
            return redirect('settings')
    context = context_dict(user=request.user, form=form)
    return render(request, 'leadfy/integrations.html', context)


def subscribe(request, username):
    user = get_object_or_404(get_user_model(), username__iexact=username)
    fields = (['name', 'email'])
    widgets = {
        'name': TextInput(attrs={'placeholder': 'Name'}),
        'email': EmailInput(attrs={'placeholder': 'Email'})
    }
    CustomForm = modelform_factory(
        model=LeadModel,
        fields=fields,
        widgets=widgets)
    form = CustomForm()

    response = redirect('thankyou', username=username)

    if request.method == 'POST':
        form = CustomForm(data=request.POST)
        form.instance.lead_from = user
        form.instance.referer = set_http_referer(request, response, username)
        form.instance.referer_main_domain = urlparse(
            set_http_referer(request, response, user.username)).netloc
        form.instance.location = get_location(request)['country_name']
        form.instance.location_code = get_location(request)['country_code']
        if form.is_valid():
            form.save()
            response.set_cookie(
                f'{user.username}_captured',
                '',
                max_age=86400 * 365)
            return response

    context = context_dict(user=user, form=form)
    return render(request, 'leadfy/emailcapture.html', context=context)


def thankyou(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    context = context_dict(user=user)
    return render(request, 'leadfy/thankyou.html', context)


def pitch(request):
    content = Pitch.objects.first()
    return render(request, 'leadfy/pitch.html', {'content': content})


@login_required
def desktopimage(request):
    preference = Preferences.objects.get(user=request.user)
    print('REQUEST RECEIVED', request.FILES.get('cropped'))
    # print(dir(request.FILES.get('cropped')))
    preference.background_image_desktop = request.FILES.get('cropped')
    preference.save()
    return JsonResponse({'success': 'success'})


@login_required
def mobileimage(request):
    preference = Preferences.objects.get(user=request.user)
    print('REQUEST RECEIVED', request.FILES.get('cropped'))
    # print(dir(request.FILES.get('cropped')))
    preference.background_image_mobile = request.FILES.get('cropped')
    preference.save()
    return JsonResponse({'success': 'success'})


def servepitchdeck(request):
    return FileResponse(open(os.path.join('media', f"documents/SelfLink's Pitch.pdf"), 'rb'))

def error_404_view(request, *args, **argv):
    response = render(request, 'leadfy/404.html')
    response.status_code = 404
    return response

def error_403_view(request, *args, **argv):
    response = render(request, 'leadfy/403.html')
    response.status_code = 403
    return response

def error_500_view(request, *args, **argv):
    response = render(request, 'leadfy/500.html')
    response.status_code = 500
    return response
