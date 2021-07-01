from django import forms
from .models import Preferences

class PreferencesForm(forms.ModelForm):

    class Meta:
        model = Preferences
        fields = '__all__'
        exclude = ['user']

        # widgets = {
        #     'primary_text_color': TextInput(attrs={'type': 'color'}),
        #     'brand_name_font_color': TextInput(attrs={'type': 'color'})
        # }
