from django.db import models

#   Classes to extend the generic django user model and make custom user models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have an username")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")

        #   If they have all the required fields, then create the user
        user = self.model(
            #   normalize_email converts all characters to lower case, available from BaseUserManager class
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        #   set_password() is a method that can be used on a user object
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            password = password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=70, unique=True)
    username = models.CharField(verbose_name="username", max_length=40, unique=True)
    first_name = models.CharField(verbose_name="first_name", max_length=30)
    last_name = models.CharField(verbose_name="last_name", max_length=30)

    #   vvv Required fields for AbstractBaseUser class vvv
    date_joined = models.DateField(verbose_name="date_joined", auto_now_add=True)
    last_login = models.DateField(verbose_name="last_login", auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    #   This USERNAME_FIELD is what the user is using to login with
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    #   Tell account object where manager is/how to use it
    objects = MyAccountManager()

    def __str__(self):
        return self.email

    #   Functions that are required for building a custom user
    #   this one gets the users permission
    def has_perm(self, perm, obj=None):
        return self.is_admin
    #   does the user have module permissions 
    def has_module_perms(self, app_label):
        return True