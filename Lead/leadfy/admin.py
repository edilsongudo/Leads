from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(LeadModel)
admin.site.register(Link)
admin.site.register(PageVisit)
admin.site.register(Preferences)
