from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [ 'username', 'email', 'role', ]
    add_fieldsets = (
        (None, {
            'fields': ('username','email', 'password1', 'password2', 'role')}
        ),
    )
    fieldsets = (
        (None, {
            'fields': ('username','email', 'role', 'password')}
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
