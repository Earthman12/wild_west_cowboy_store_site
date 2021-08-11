from django.shortcuts import render
from operator import attrgetter
from store_front.models import Product
from blog.models import BlogPost

# Create your views here.

def store_home_view(request):
    
    context = {}

    #   A 'select all query' from the database and passing it as context
    products = Product.objects.all()
    context['products'] = products

    #   Query all the blog posts but we want to sort them. This line is going to query all the blog_posts and then sort the list based on the key 'date_updated' and then it will reverse it so the newest post will be at the top
    blog_posts = sorted(BlogPost.objects.all(), key = attrgetter('date_updated'), reverse = True)
    context['blog_posts'] = blog_posts

    return render(request, 'store_front/store_home.html', context)