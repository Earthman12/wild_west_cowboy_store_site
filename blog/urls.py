from django.urls import path
from blog.views import (
    create_blog_view,
)

#   Whenever url file is created that is not in the main url file (i.e. its in an app like 'blog'), it must have an 'app_name' parameter
app_name = 'blog'

urlpatterns = [
    path('create/', create_blog_view, name =  "create")
]