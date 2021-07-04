from .forms import PageForm
from .models import LeadModel, Page, PageVisit
from django.forms.models import modelform_factory
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
import json
from django.http import FileResponse, JsonResponse


def home(request):
    if request.user.is_authenticated:

        def number_of_clicks():
            number_of_clicks = 0
            pages = Page.objects.filter(user=request.user)
            for page in pages:
                number_of_clicks += page.view_count
            return number_of_clicks

        def number_of_leads():
            number_of_clicks = 0
            number_of_leads = LeadModel.objects.filter(lead_from=request.user).count()
            print(number_of_leads)
            return number_of_leads

        def hours():
            hours = []
            for i in range(0, 24):
                pages_visits = PageVisit.objects.filter(
                    page__user=request.user, time__hour=i)
                hours.append(len(pages_visits))
            return hours

        if request.is_ajax():
            return JsonResponse({'page_views': number_of_clicks(), 'clicks_per_hours': hours(), 'number_of_leads': number_of_leads()})

        return render(request, 'leadfy/dash.html')

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
