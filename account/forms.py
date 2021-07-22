from django import forms

#   Built in class with Django to help build form for authenticating users
from django.contrib.auth.forms import UserCreationForm
#   The authenticate method checks to see if users credentials are valid
from django.contrib.auth import authenticate
from django.forms import fields


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
        #   Need to check if the form is valid or essentially check that a proper email is inputted
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            if not authenticate(email = email, password = password):
                raise forms.ValidationError("Invalid Login Credentials")

#   Form for updating user accounts
class AccountUpdateForm(forms.ModelForm):

    #   There are no parameters because we don't have a password
    class Meta:
        model: Account
        #   These are the fields that you want to be able to change
        fields = ('email', 'username')
    
    #   Instead of using clean() and go through all the properties of the form like above, we can clean individual properties in the form instead
    #   clean_email() will just reference the email and whether the form is valid or not, it will run the method to apply any extra logic you want it to
    def clean_email(self):
        #   Want to make sure the form is valid first and then check the email so that it doesn't equal another email thats already in the database
        if self.is_valid():
            email = self.cleaned_data['email']
            #   Check to see if the account exists
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            #   If the account does not exists then it is good to go, and we return the email and we can update the account to the new email
            except Account.DoesNotExist:
                return email
            #   Otherwise raise an error
            raise forms.ValidationError('Email "%s" already in use.' % account.email)#  Could also just write email since it's already a variable above

    #   ^^^^^Do the same thing for the username that was done for the email above^^^^^
    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" already in use.' % account.username)