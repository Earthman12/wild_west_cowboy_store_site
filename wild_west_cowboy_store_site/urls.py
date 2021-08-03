"""wild_west_cowboy_store_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#   Using these django prepackaged to change the users password views but make a few changes
from django.contrib.auth import views as auth_views

from store_front.views import (
    store_home_view,
)

from account.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', store_home_view, name = "home"),
    path('register/', registration_view, name = "register"),
    path('logout/', logout_view, name = "logout"),
    path('login/', login_view, name = "login"),
    path('account/', account_view, name = "account"),
    path('blog/', include('blog.urls', 'blog')),#  This will add all of 'blogs' urls
    
    #   These urls were copied from the django source code from https://github.com/django/django/blob/main/django/contrib/auth/urls.py 
    #   The urls for login and logout were already made created because they we created seperately so they did not need to be copied here because here we are referencing prebuilt django views
    #   This has to be done because we chose to make a custom user account rather than use djangos
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),#In order to customize the view, we have to pass in 'template_name' to the view we reference which are custom built

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

#   If we are in a devoloper environment
if settings.DEBUG:
    #   Reference the static directories
    urlpatterns += static(settings.STATIC_URL, documnent_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, documnent_root = settings.MEDIA_ROOT)
    #   This tells the project where the static_url/media_url/root is if we are in debug mode