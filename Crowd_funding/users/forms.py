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
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits long.")
        return phone


class YourLoginForm(AuthenticationForm):
    pass 

    