from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView
from .models import Product

#======================= REGISTER USER
def registerUser(request):  
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, 'register.html')

#======================= LOGIN
def userLogin(request):
    context = {}
    return render(request, 'login.html', context)

#======================= CATEGORY / LIST_PRODUCTS
def listProducts(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'catalog/list_products.html', context)

#======================= SINGLE PRODUCT
class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_details.html'