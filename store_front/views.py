from django.shortcuts import render

# Create your views here.

def store_home_view(request):
    print(request.headers)
    return render(request, 'store_front/store_home.html', {})