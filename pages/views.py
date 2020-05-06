from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_view(request):
    print(request.user)
    return HttpResponse("<h1>Hello world</h1>")

def list_products(request):
    return render(request, 'list_products.html')