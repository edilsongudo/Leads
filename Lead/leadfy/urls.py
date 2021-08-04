from django.urls import path
from leadfy.views import *
from django.contrib.sitemaps.views import sitemap
from leadfy.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap
}

urlpatterns = [
    path('', home, name="home"),
    path('preferences/', preferences, name="preferences"),
    path('settings/', settings, name="settings"),
    path('leads/see/', leads, name="leads"),
    path('dashboard/<str:days>', dashboard, name="dashboard"),
    path('link/create/', createlink, name="link-create"),
    path('link/<str:short_url>/edit/', editlink, name="link-edit"),
    path('link/<int:pk>/delete/',
         LinkDeleteView.as_view(), name="link-delete"),
    path('<str:short_url>/', lead, name="lead"),
    path('u/<str:username>/', landing, name="user-landing"),
    path('u/<str:username>/edit', landing_as_author_pv,
         name="landing_as_author_pv"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps})
]


from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
