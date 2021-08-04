from django import forms

from blog.models import BlogPost

class CreateBlogPostForm(forms.ModelForm):

    class Meta:
        #   Tell it what to model the form after (i.e. after a blog post) and the fields we are interested in (the fields that users can actually change)
        model = BlogPost
        fields = ['title', 'body', 'image']