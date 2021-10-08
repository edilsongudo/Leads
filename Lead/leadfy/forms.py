from django import forms
from .models import *
from django.forms.widgets import TextInput

class LinkCreateForm(forms.ModelForm):

    class Meta:
        model = Link
        fields = '__all__'
        exclude = ['user', 'view_count', 'description']

        labels = {
            'short_url': 'selflink.link/to/'
        }

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
        fields = ['background_image_mobile',
                  'background_image_desktop']

class AdvancedForm(forms.ModelForm):

    class Meta:
        model = Advanced
        fields = '__all__'
        exclude = ['user']

        help_message = '''If Zero, visitors always will be asked to subscribe everytime
         they click a link with with "ask visitors to subscribe" turned On'''

        help_texts = {
            'seconds_to_wait_before_asking_user_to_subscribe_again': help_message
        }


class SubscribeButtonForm(forms.ModelForm):

    class Meta:
        model = SubscribeButton
        fields = '__all__'
        exclude = ['user']

        help_texts = {
            'show': '''Whether to show this button or not in your bio page'''
        }

        widgets = {
            'call_to_action': forms.Textarea(attrs={
                'rows': 5
            })
        }


class PitchForm(forms.ModelForm):

    class Meta:
        model = Pitch
        fields = '__all__'
