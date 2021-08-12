from django import forms

from blog.models import BlogPost

class CreateBlogPostForm(forms.ModelForm):

    class Meta:
        #   Tell it what to model the form after (i.e. after a blog post) and the fields we are interested in (the fields that users can actually change)
        model = BlogPost
        fields = ['title', 'body', 'image']



#   A form for editing blog posts
class UpdateBlogPostForm(forms.ModelForm):

    #   Override Meta and set model to the blog post and the fields to the fields we want to edit/update
    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image']

    #   A save function which will only be called if 'commit' is equal to true, this is a custom 'save' method for the form to specify the fields that are being changed
    def save(self, commit = True):

        #   Blog post reference
        blog_post = self.instance
        #   Get blog post title and body
        blog_post.title = self.cleaned_data['title']
        blog_post.body = self.cleaned_data['body']

        #   If the form has a new image, set the new image otherwise don't change the current one
        if self.cleaned_data['image']:
            blog_post.image = self.cleaned_data['image']

        if commit:
            blog_post.save()

        return blog_post        