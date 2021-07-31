from django.contrib import admin
from .models import Profile

from django.contrib.auth import admin as auth_admin
from .forms import UserChangeForm, UserCreationForm
from .models import User

admin.site.register(Profile)


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        ("Informações Pessoais", {"fields": ("bio",)}),
    )
