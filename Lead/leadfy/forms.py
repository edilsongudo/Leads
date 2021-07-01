from django import forms
from .models import *


class LeadForm(forms.ModelForm):
    # email = forms.EmailField()

    class Meta:
        model = LeadModel
        fields = ['name', 'email']
