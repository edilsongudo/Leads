from django.urls import path
from leadfy.views import *
from django.contrib.sitemaps.views import sitemap
from leadfy.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap
}

urlpatterns = [
    path('', home, name="home"),
    path('mobile/upload/', mobileimage, name="mobileimage"),
    path('desktop/upload/', desktopimage, name="desktopimage"),
    path('preferences/', preferences, name="preferences"),
    path('settings/', settings, name="settings"),
    path('advanced/', advanced, name="advanced"),
    path('leads/', leads, name="leads"),
    path('dashboard/<str:days>', dashboard, name="dashboard"),
    path('link/create/', createlink, name="link-create"),
    path('link/<str:short_url>/edit/', editlink, name="link-edit"),
    path('link/<str:short_url>/delete/', deletelink, name="link-delete"),
    path('p/<str:short_url>', lead, name="lead"),
    path('<str:username>/', landing, name="user-landing"),
    path('<str:username>/edit', landing_as_author_pv,
         name="landing_as_author_pv"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps})
]


from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
