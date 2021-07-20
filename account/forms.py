from django import forms

#   Built in class with Django to help build form for authenticating users
from django.contrib.auth.forms import UserCreationForm

from account.models import Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=70, help_text="Valid email address is required")

    #   Telling the registration form what kind of data it will be modeling/what it will look like so it will all the required fields inside of the Account model
    class Meta:
        model = Account
        fields = ("email", "username", "first_name", "last_name", "password1", "password2")