from django.urls import path
from leadfy.views import *
from django.contrib.sitemaps.views import sitemap
from leadfy.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap
}

urlpatterns = [
    path('', home, name="home"),
    path('dashboard/<str:days>', dashboard, name="dashboard"),
    path('page/create/', createpage, name="page-create"),
    path('page/<str:code>/edit/', editpage, name="page-edit"),
    path('<str:code>/', lead, name="lead"),
    path('u/<str:username>/', landing, name="user-landing"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps})
]


from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
