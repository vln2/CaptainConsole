from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Category, ProductImage
from django.db.models import F
from .forms import CreatingUserForms


def registerUser(request):
    #if request.user.is_authenticed:
    #    return redirect('base')
    form = CreatingUserForms()
    #else:
    if request.method == 'POST':
        form = CreatingUserForms(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account has been made, Welcome ' + user)
            return redirect('login')

    return render(request, 'pages/register.html', {'form': form})

def userLogin(request):
    #if request.user.is_authenticed:
    #    return redirect('login')
    #else:
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


def userLogout(request):
    logout(request)
    return redirect('login')


def productList(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'pages/product_list.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'pages/product_details.html'

    def get_object(self):
        iProductId = self.kwargs['id']
        return {
            'product': Product.objects.get(id=iProductId),
            'gallery': ProductImage.objects.filter(product=iProductId)
        }


def show_category(request, hierarchy=None):
    categories_slug = hierarchy.split('/')
    category_slug = categories_slug[-1]
    category = Category.objects.get(slug=category_slug)

    context = {
        'instance': category,
        'products': category.get_products,
        'breadcrumbs': category.get_ancestors(include_self=True)
    }
    return render(request, 'pages/product_list.html', context)

#passa að bæta við @login_required(login_url='login') ef notandi þarf að vera skráður inn til að gera einhvað ákveðið
