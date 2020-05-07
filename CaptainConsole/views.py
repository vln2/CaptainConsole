from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .models import Product

#======================= REGISTER USER
def register_user(request):  
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, 'register.html')

#======================= LOGIN
def user_login(request):
    context = {}
    return render(request, 'login.html', context)

#======================= CATEGORY / LIST_PRODUCTS
def list_products(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'catalog/list_products.html', context)

#======================= SINGLE PRODUCT
def single_product(response, id):

    context = {
        'product': Product.objects.get(id=id)
    }
    print(context['product'])
    return render(response, 'product/single_product.html', context)
