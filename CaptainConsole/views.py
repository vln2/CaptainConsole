from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

#views created
from .models import Product

def register_user(request):  
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, 'templates/register.html', context)

def user_login(request):
    context = {}
    return render(request, 'templates/login.html', context)    

def list_products(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'list_products.html', context)
