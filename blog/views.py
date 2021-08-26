from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q  # 'Q lookup' for searching
from django.http import HttpResponse
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from blog.models import BlogPost
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm
from account.models import Account

#   Constant we define, is 1 for testing
BLOG_POSTS_PER_PAGE = 5

# Create your views here.

def blog_home_view(request):

    context = {}

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

    return render(request, "blog/blog_home.html", context)


def create_blog_view(request):

    context = {}

    user = request.user

    #   If the user is not authenticated, we redirect them to a page that tells them they need to be authenticated to create a blog post
    if not user.is_authenticated:
        return redirect('must_authenticate')

    #   It will be a post request or nothing at all and because they are going to be able to upload an image the 'request.FILES' parameter to the form
    form = CreateBlogPostForm(request.POST or None, request.FILES or None)

    #   If the form is valid, we do some things and save it
    if form.is_valid():
        #   'obj' creates the form after fields have been validated and we do this becase we set the author object to the blog post, is not set by default
        obj = form.save(commit = False)
        #   This will get the first item from the query set(should only be one) which should be the user
        author = Account.objects.filter(email = user.email).first()

        #   Set the author and save the blog post into the database
        obj.author = author
        obj.save()

        #   Reset everything by setting the form to a brand new blog post form
        form = CreateBlogPostForm()

    context['form'] = form

    return render(request, "blog/create_blog.html", context)



def detail_blog_view(request, slug):

    context = {}
    #   Will get the object or throw 404 error
    blog_post = get_object_or_404(BlogPost, slug = slug)
    context['blog_post'] = blog_post
    
    return render(request, 'blog/detail_blog.html', context)



def edit_blog_view(request, slug):
    
    context = {}

    user = request.user

    #   Check if user is authenticated
    if not user.is_authenticated:
        return redirect("must_authenticate")

    #   Check for the blog post
    blog_post = get_object_or_404(BlogPost, slug = slug)

    #   Check to see if the author of the blog is the current user
    if blog_post.author != user:
        return HttpResponse("Whoa slow your horses there partner, you don't seem to be writer of this post")

    if request.POST:
        #   Just like above ^^^^^^ It will be a post request or nothing at all and because they are going to be able to upload an image the 'request.FILES' parameter to the form
        form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance = blog_post)# 'blog_post' must be passed as the 'instance' 

        if form.is_valid():
            obj = form.save(commit = False)#This will load parameters into form giving access to the 'cleaned_data'
            obj.save()
            context['success_message'] = "Updated"
            blog_post = obj

    #   Setting initial values, this was done in the 'account' view
    form = UpdateBlogPostForm(
        initial={
            "title" : blog_post.title,
            "body" : blog_post.body,
            "image" : blog_post.image,
        }
    )

    context['form'] = form

    return render(request, 'blog/edit_blog.html', context)



#   A function for getting a query set based on a particular search
def get_blog_queryset(query = None):
    #   'queryset' is a list
    queryset = []
    #   'queries' is a list of all the queries that were entered by the user. This takes whatever is entered and removes all the whitespace and puts it in a list and search them individually. Ex) django latest documentation = [django, latest, documentation] 
    queries = query.split(" ")

    for q in queries:
        #   This will search for posts and will use 'Q lookup' to search 
        posts = BlogPost.objects.filter(
            #   'icontains' will get rid of any capitalization
            Q(title__icontains = q)  |
            Q(body__icontains = q)
        ).distinct()    #'distinct()' will make sure all of the posts in the list that is retrieved is unique
        
        #   Loop through each post and append the post to a queryset
        for post in posts:
            queryset.append(post)

    #   return the list but as a unique list. 'set' will make sure it's unique and then converting to a list to send to the template
    return list(set(queryset))