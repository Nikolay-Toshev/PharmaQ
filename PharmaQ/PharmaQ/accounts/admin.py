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

    list_display = ('username', 'email', 'is_patient', 'is_pharmacist', 'is_active', 'is_staff')

    search_fields = ('username', 'email', 'first_name', 'last_name')

    list_filter = ('groups', 'is_pharmacist', 'is_patient', 'is_active', 'is_staff')

    fieldsets = (
        (None, {'fields': ('username','email', 'password')}),
        ('Permissions', {'fields': ('is_pharmacist', 'is_patient', 'is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Login Info', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

