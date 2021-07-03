from django.contrib import admin
from .models import LeadModel, Page, PageVisit

# Register your models here.
admin.site.register(LeadModel)
admin.site.register(Page)
admin.site.register(PageVisit)
