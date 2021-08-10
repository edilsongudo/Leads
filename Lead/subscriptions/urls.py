from django.urls import path
from .views import *


urlpatterns = [
    path('subscribe/', subscribe, name="subscribe"),
    path('activate/<subID>/', activate, name="activate"),
    path('deactivate/<subID>/', deactivate, name="deactivate")
]
