from django.urls import path
from blog.views import (
    create_blog_view,
    detail_blog_view,
    edit_blog_view,
)

#   Whenever url file is created that is not in the main url file (i.e. its in an app like 'blog'), it must have an 'app_name' parameter
app_name = 'blog'

urlpatterns = [
    path('create/', create_blog_view, name =  "create"),
    #   '<slug>' will make the url the slug name of the blog post
    path('<slug>/', detail_blog_view, name =  "detail"),
    path('<slug>/edit', edit_blog_view, name =  "edit"),
]