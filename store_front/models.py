from django.db import models


# Create your models here.

#   Function for defining the upload location for the images that will be associated with the product. This is taken from blog model
def upload_location(instance, filename, **kwargs):
    #   'product_name' is the name of the product, 'filename' is the name of file that comes from the computer of the one who uploads it. .format() converts it all to a string
    file_path = 'store_home/{product_name}-{filename}'.format(product_name = str(instance.name), filename = filename
    )
    return file_path

class Product(models.Model):

    name = models.CharField(verbose_name="name", max_length=50)
    stock = models.IntegerField(verbose_name="stock", default=0)
    description = models.CharField(verbose_name="description", max_length=100)
    price = models.FloatField(verbose_name="price", default=0.0)
    image = models.ImageField(upload_to = upload_location, null = False, blank = False)#This cant be used unless Pillow library is used

    def __str__(self):
        return self.name

    #   This changes the display names in admin page
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"