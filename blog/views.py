from django.shortcuts import get_object_or_404, render, redirect

from blog.models import BlogPost
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm
from account.models import Account

# Create your views here.

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