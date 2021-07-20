from django import forms

#   Built in class with Django to help build form for authenticating users
from django.contrib.auth.forms import UserCreationForm
#   The authenticate method checks to see if users credentials are valid
from django.contrib.auth import authenticate


from account.models import Account

#   Form for registering users
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=70, help_text="Valid email address is required")

    #   Telling the registration form what kind of data it will be modeling/what it will look like so it will all the required fields inside of the Account model
    class Meta:
        model = Account
        fields = ("email", "username", "first_name", "last_name", "password1", "password2")

#   Form for authenticating users
class AccountAuthenticationForm(forms.ModelForm):

    #   The forms.PasswordInput specifies that it is a password field and will not be visible when they are inputting it
    password = forms.CharField(label = 'Password', widget = forms.PasswordInput)

    #   Telling it what kind of fields to see in the form and which fields will be visible
    class Meta:
        model = Account
        fields = ('email', 'password')

    #   It is available to any form that extends the model form. Acts as an interceptor, before the form can do anything it has to run the clean() method and then any logic that is in the clean() method will get executed before the form can do anything and is useful to make sure a users credentials are valid and if they are not then we can provide feedback
    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(email = email, password = password):
            raise forms.ValidationError("Invalid Login Credentials")