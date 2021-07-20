from django.db import models


# Create your models here.
class Product(models.Model):

    name = models.CharField(verbose_name="name", max_length=50)
    stock = models.IntegerField(verbose_name="stock", default=0)
    description = models.CharField(verbose_name="description", max_length=100)
    price = models.FloatField(verbose_name="price", default=0.0)

    def __str__(self):
        return self.name

    #   This changes the display names in admin page
    class Meta:
        verbose_name = "The Product"
        verbose_name_plural = "All the Products"