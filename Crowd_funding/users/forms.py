# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from adminpanel.models import user_signup

from django.core.validators import MinLengthValidator

from django.contrib.auth.forms import UserCreationForm


class UserSignupForm(UserCreationForm):
    class Meta:
        model = user_signup
        fields = ['username', 'name', 'email', 'phone']


class YourLoginForm(AuthenticationForm):
    pass 

    