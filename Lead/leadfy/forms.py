from django import forms
from .models import *
from django.forms.widgets import TextInput

class LinkCreateForm(forms.ModelForm):

    class Meta:
        model = Link
        fields = '__all__'
        exclude = ['user', 'view_count']

class LinkEditForm(forms.ModelForm):

    class Meta:
        model = Link
        fields = '__all__'
        exclude = ['user', 'view_count', 'short_url']

        # widgets = {
        #     'primary_text_color': TextInput(attrs={'type': 'color'}),
        #     'brand_name_font_color': TextInput(attrs={'type': 'color'})
        # }

class PreferencesForm(forms.ModelForm):

    class Meta:
        model = Preferences
        fields = ['font_family', 'background_image', 'use_background_image']
