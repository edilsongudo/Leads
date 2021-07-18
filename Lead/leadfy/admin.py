from django.contrib import admin
from .models import LeadModel, Link, PageVisit

# Register your models here.
admin.site.register(LeadModel)
admin.site.register(Link)
admin.site.register(PageVisit)
