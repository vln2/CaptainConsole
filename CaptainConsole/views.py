from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Category, ProductImage, Order, Item
from django.db.models import F
from .forms import CreatingUserForms, AddItemToCartForm


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
    products = category.get_products()
    paginator = Paginator(products, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'add_to_cart_form': AddItemToCartForm(),
        'instance': category,
        'products': page_obj,
        'breadcrumbs': category.get_ancestors(include_self=True)
    }

    return render(request, 'pages/product_list.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = AddItemToCartForm(request.POST or None)
    if form.is_valid():

        order_qs = Order.objects.filter(owner=request.user, status=Order.CART)
        if order_qs.exists():
            order = order_qs[0]
        else:
            order = Order.objects.create(owner=request.user)

        item_qs = order.items.filter(product__id=product.id)
        if item_qs.exists():
            item = item_qs[0]
            item.quantity += 1
            item.save()
            messages.info(request, "This item quantity was updated.")
            # return redirect("core:order-summary")
        else:
            item = Item.objects.create(product=product)
            order.items.add(item)
            messages.info(request, "This item was added to your cart.")
            # return redirect("core:order-summary")

    httpheaders = request.headers
    refer = httpheaders['Referer']
    return redirect(refer)