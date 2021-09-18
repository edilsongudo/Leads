from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('footballisawesome/', admin.site.urls),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path("accounts/", include("allauth.urls")),
    path('premium/', include('subscriptions.urls')),
    path('profile/', include('users.urls')),
    path('', include('leadfy.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'leadfy.views.error_404_view'
