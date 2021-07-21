from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from account.forms import AccountAuthenticationForm, RegistrationForm


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
            #login(request, account)

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

def login_view(request):
    context = {}

    user = request.user

    #   Check to see if user is authenticated, they shouldn't be at the login screen. Redirect to the home screen
    if user.is_authenticated:
        return redirect("home")

    #   If they are not authenticated and are trying to login, then proceed 
    if request.POST:
        form = AccountAuthenticationForm(request.POST)

        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            
            #   then want to authenticate the user
            user = authenticate(email = email, password = password)

            #   check to see if the user object exists i.e. the user was successfully authenticated, then login the user
            if user:
                login(request, user)
                return redirect('home')

    #   What if it is not a POST request, then the user is viewing the login page and they have not attempted to login yet and they are not authenticated
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, 'account/login.html', context)
    