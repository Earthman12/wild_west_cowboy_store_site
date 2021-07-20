from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from account.forms import RegistrationForm

# Create your views here.
def registration_view(request):
    context = {}
    #   if it is a POST request, set the form
    if request.POST:
        form = RegistrationForm(request.POST)
        #   if there are no errors with users input (the user entered correct username/email, passwords match, etc..), then save it
        if form.is_valid():
            form.save()
            #   the way to get data from a valid form, the parameters('email' and 'password' are from forms.py)
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            #   then want to authenticate the account, it will determine if the credentials are valid and then will create the user object
            account = authenticate(email=email, password=raw_password)
            #   once we have user object we call login and pass the request and the account and then we redirect to the home store page
            login(request, account)
            return redirect('home')

        #   if the form was not valid, if there were issues with the form, pass the form to the template to display errors
        else:
            #   add form to the context
            context['registration_form'] = form
    
    #   if the request is not a POST request, it is a GET and they are visiting for the first time
    else:
        #   Want to see RegistrationForm() w/out POST request being passed to it. Still want to add 'registration_form' to the context
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'account/register.html', context)

#   View for logging out
def logout_view(request):
    logout(request)
    return redirect('home')
