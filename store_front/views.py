from django.shortcuts import render
from store_front.models import Product

# Create your views here.

def store_home_view(request):
    
    context = {}

    #   A 'select all query' from the database and passing it as context
    products = Product.objects.all()
    context['products'] = products

    return render(request, 'store_front/store_home.html', context)