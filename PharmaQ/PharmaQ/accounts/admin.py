from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from PharmaQ.accounts.forms import AppUserRegistrationForm, AppUserChangeForm

UserModel = get_user_model()

@admin.register(UserModel)
class UserModelAdmin(UserAdmin):
    model = UserModel
    add_form = AppUserRegistrationForm
    form = AppUserChangeForm

    fieldsets = (
        (None, {'fields': ('username','email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_approved', 'groups', 'user_permissions', )}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )