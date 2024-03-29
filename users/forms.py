from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields =  ('username', 'first_name', 'last_name', 'email','role',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields =  ('first_name', 'last_name', 'email','role',)

