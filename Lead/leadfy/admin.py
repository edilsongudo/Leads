from django.contrib import admin
from .models import LeadModel, Preferences

# Register your models here.
admin.site.register(LeadModel)
admin.site.register(Preferences)
