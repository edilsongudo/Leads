from .forms import PageForm
from .models import LeadModel, Page, PageVisit
from django.forms.models import modelform_factory
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
import json
from django.http import FileResponse, JsonResponse
import datetime



def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard', days='0')
    else:
        return render(request, 'leadfy/home.html')


def landing(request, username):
    user = get_object_or_404(User, username=username)
    pages = Page.objects.filter(user=user)
    return render(request, 'leadfy/index (2).html', {'user': user, 'pages': pages})


@login_required
def createpage(request):
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'leadfy/page.html', {'form': form})


@login_required
def editpage(request, code):
    page = get_object_or_404(Page, code=code)
    form = PageForm(instance=page)
    # if request.user.username == page.user.username:
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'leadfy/page.html', {'form': form})
    # else:
    #     return HttpResponseForbidden()


def lead(request, code):
    page = get_object_or_404(Page, code=code)
    user = page.user
    fields = (['name', 'email'])
    CustomForm = modelform_factory(model=LeadModel, fields=fields)
    form = CustomForm()
    if request.method == 'POST':
        if 'skip' in request.POST:
            return redirect(page.link)
        form = CustomForm(data=request.POST)
        form.instance.lead_from = user
        if form.is_valid():
            form.save()
            return redirect(page.link)

    response = render(request, 'leadfy/forms/myform/index.html',
                      {'form': form, 'user': user, 'page': page})
    if not code in request.COOKIES:
        response.set_cookie(code, code)
        page.view_count += 1
        page.save()
        new_visit = PageVisit(page=page)
        new_visit.save()
    return response


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

    return render(request, 'leadfy/dash.html')
