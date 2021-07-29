from django.db import models

#   Extra libraries needed for this class
from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver

# Create your models here.

#   Function for defining the upload location for the images that will be associated with the blog post
def upload_location(instance, filename, **kwargs):
    #   'author_id' is the person who made the blog post, 'title' is title of the blog post, 'filename' is the name of file that comes from their computer when the user uploads it. .format() converts it all to a string
    file_path = 'blog/{author_id}/{title}-{filename}'.format(
        author_id = str(instance.author.id), title = str(instance.title), filename = filename
    )
    return file_path

class BlogPost(models.Model):
    title = models.CharField(max_length = 60, null = False, blank = False) #null and false are False because it cant have a null or a blank title i.e. title is required
    body = models.TextField(max_length = 2500, null = False, blank = False)
    image = models.ImageField(upload_to = upload_location, null = False, blank = False)#This cant be used unless Pillow library is used
    date_published = models.DateTimeField(auto_now_add = True, verbose_name = "date published")#auto_now_add inserts a time stamp as soon as object is created
    date_updated = models.DateTimeField(auto_now = True, verbose_name = "date updated")#auto_now makes it so this time stamp only changes when the object changes/is updated
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)#Use a foreign key relationship to tie this field to the 'account' table. 'on_delete' defines what happens if the blog post is deleted. models.CASCADE means delete anything that is associated with this blog post
    slug = models.SlugField(blank = True, unique = True)#A slug is a URL, can't be any other URL that has the same one so it has to be 'unique'

    def __str__(self):
        return self.title

#   These are extras that are needed to do certain things given certain circumstances

#   What this does is if this BlogPost is deleted, it will delete the image that is associated with it
@receiver(post_delete, sender = BlogPost)#'post_delete' is referencing an import from above
def submission_delete(sender, instance, **kwargs):#Signal recievers must accept keyword arguments
    instance.image.delete(False)

#   This is called before the blog post is committed to the database, this intercepts the saving of the blog post to the database and can execute some action before it is saved. This makes a slug before it is saved
def pre_save_blog_post_reciever(sender, instance, *args, **kwargs):#Signal recievers must accept keyword arguments
    if not instance.slug:#if there is no slug created
        instance.slug = slugify(instance.author.username + "-" + instance.title)#'slugify' is a function for creating a slug. This makes sure that this blog post is unique

#   Wire pre_save receiver
pre_save.connect(pre_save_blog_post_reciever, sender = BlogPost)#Whenever a blog post is attempted to be saved into the database, call 'pre_save_blog_post_reciever' and use 'BlogPost' model as its sender