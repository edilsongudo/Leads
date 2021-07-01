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
    path('<str:username>/', lead, name="lead"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps})
]


from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
