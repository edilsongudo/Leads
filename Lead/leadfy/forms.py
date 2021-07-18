from django import forms
from .models import Link

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
