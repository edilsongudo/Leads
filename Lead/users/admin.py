from django.contrib import admin
from .models import Profile

from django.contrib.auth import admin as auth_admin
from .forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
admin.site.register(Profile)


@admin.register(get_user_model())
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = get_user_model()
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        ("Informações Pessoais", {"fields": ("bio",)}),
    )
