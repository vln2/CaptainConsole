from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#======================= VIEWS CREATED
from .models import Product
from .forms import CreatingUserForms

#======================= REGISTER USER
def registerUser(request):  
    if request.user.is_authenticed:
        return redirect('base')
        form = CreatingUserForms()
    else:
        if request.method == 'POST':
            form = CreatingUserForms(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account has been made, Welcome ' +  user)
                return redirect('login')

        return render(request, 'pages/register.html')

#======================= LOGIN
def userLogin(request):
    if request.user.is_authenticed:
        return redirect('login')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
        
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, username)
                return redirect('home')
            else: 
                messages.info(request, 'Your username OR password is incorrect')
        context = {}
        return render(request, 'pages/login.html', context)

#======================= USER LOG OUT
def userLogout(request):
    logout(request)
    return redirect('login')

#======================= CATEGORY / LIST_PRODUCTS
def productList(request):
    aProducts = Product.objects.all()
    context = {
        'products': aProducts
    }
    return render(request, 'pages/product_list.html', context)

#======================= SINGLE PRODUCT
class ProductDetailView(DetailView):
    model = Product
    template_name = 'pages/product_details.html'


#passa að bæta við @login_required(login_url='login') ef notandi þarf að vera skráður inn til að gera einhvað ákveðið