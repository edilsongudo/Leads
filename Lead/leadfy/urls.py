from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from leadfy.views import *
from django.contrib.sitemaps.views import sitemap
from leadfy.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap
}

urlpatterns = [
    path('', home, name="home"),
    path('<str:username>/subscribe', subscribe, name="subscribe"),
    path('<str:username>/thankyou/', thankyou, name="thankyou"),
    path('socials/', socials, name="socials"),
    path('integrations/', integrations, name="integrations"),
    path('mobile/upload/', mobileimage, name="mobileimage"),
    path('desktop/upload/', desktopimage, name="desktopimage"),
    path('preferences/', preferences, name="preferences"),
    path('settings/', settings, name="settings"),
    path('export/', export, name="export"),
    path('subscribebutton-edit/', subscribebutton, name="subscribebutton"),
    path('advanced/', advanced, name="advanced"),
    path('exportleads/', exportleads, name="exportleads"),
    path('exportlinks/', exportlinks, name="exportlinks"),
    path('exportlink/<str:short_url>/', exportlink, name="exportlink"),
    path('dashboard/<str:days>', dashboard, name="dashboard"),
    path('link/create/', createlink, name="link-create"),
    path('link/<str:short_url>/edit/', editlink, name="link-edit"),
    path('link/<str:short_url>/delete/', deletelink, name="link-delete"),
    path('to/<str:short_url>', lead, name="lead"),
    path('<str:username>/', landing, name="user-landing"),
    path('<str:username>/edit', landing_as_author_pv,
         name="landing_as_author_pv"),
    path('<str:username>/stats/', stats, name="stats"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('pitch/read/', pitch, name="pitch"),
]
