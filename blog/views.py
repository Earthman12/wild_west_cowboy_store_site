from django.shortcuts import render, redirect

from blog.models import BlogPost
from blog.forms import CreateBlogPostForm
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