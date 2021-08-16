from .views import *
from django.urls import path, include

urlpatterns = [
    path('', profile, name="profile"),
    path('upload/', profileimage, name="profileimage"),
]
