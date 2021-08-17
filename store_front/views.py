from django.shortcuts import render
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from store_front.models import Product
from blog.models import BlogPost
from blog.views import get_blog_queryset

#   Constant we define, is 1 for testing
BLOG_POSTS_PER_PAGE = 5

# Create your views here.

def store_home_view(request):
    
    context = {}

    #   A 'select all query' from the database and passing it as context
    products = Product.objects.all()
    context['products'] = products
    
    #   Functionality to accept a query as input
    query = ""
    #   If it is a get request
    if request.GET:
        #   Search for the parameter 'q'. This will get the value of 'q', if it is nothing, give it default value of nothing ''. Prevents issues with empty parameters from the url
        query = request.GET.get('q', '')
        #   Whether or not we have/find parameter 'q' we return it to the template to display in the search bar
        context['query'] = str(query)

    #   Query all the blog posts but we want to sort them. This line is going to query all the blog_posts and then sort the list based on the key 'date_updated' and then it will reverse it so the newest post will be at the top
    blog_posts = sorted(get_blog_queryset(query), key = attrgetter('date_updated'), reverse = True)
    #context['blog_posts'] = blog_posts

    #   Pagination, the structure of it will usually be the same for most sites. Only changes are the parameter names and the query set that is passed to the input of the paginator
    #   Get the property 'page' and set a default value of 1
    page = request.GET.get('page', 1)
    #   
    blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)

    try:
        blog_posts = blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
    except EmptyPage:
        blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

    context['blog_posts'] = blog_posts

    return render(request, 'store_front/store_home.html', context)