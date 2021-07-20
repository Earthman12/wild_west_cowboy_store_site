from django.contrib import admin

#   A helper class for making admin screens
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from account.models import Account

class AccountAdmin(UserAdmin):
    #   What you want displayed as columns in admin site
    list_display = ('email', 'username', 'date_joined', 'is_admin', 'is_staff')
    #   Creates search bar in admin console and specify the fields to query the database for
    search_fields = ('email', 'username')
    #   Fields that are read only and should be able to be changed
    readonly_fields = ('date_joined', 'last_login')
    #   Don't want any filter horizontal options so set it to nothing
    filter_horizontal =()
    #   More filtering options
    list_filter = ()
    #   Unsure of what fieldsets() does but is required
    fieldsets = ()

admin.site.register(Account, AccountAdmin)