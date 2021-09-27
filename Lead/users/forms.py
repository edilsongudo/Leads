from django import forms
# from django.contrib.auth.models import User
from users.models import User
# from django.contrib.auth.forms import UserCreationForm
from .models import Profile


from django.contrib.auth import forms as auth_forms
from .models import User


class UserChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = User


class UserUpdateForm(forms.ModelForm):
    # email = forms.EmailField()

    class Meta:
        model = User
        # fields = ['username', 'email']
        fields = ['username']

        labels = {
            'username': 'URL: selflink.link/'
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'bio']

        labels = {
            'name': 'Display Name'
        }

        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 5
            })
        }


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
