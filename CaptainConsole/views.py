from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Category, ProductImage, Order, Item
from .forms import CreatingUserForms, AddItemToCartForm, LoginForm
from django.db.models import Q

# ======================= REGISTER USER
def registerUser(request):
    #if request.user.is_authenticed:
    #    return redirect('base')
    registerForm = CreatingUserForms()
    #else:
    if request.method == 'POST':
        registerForm = CreatingUserForms(request.POST)
        if registerForm.is_valid():
            registerForm.save()
            user = registerForm.cleaned_data.get('username')
            messages.success(request, 'Account has been made, Welcome ' + user)
            return redirect('login')

    return render(request, 'pages/register.html', {'form': registerForm})

# ======================= LOGIN
def userLogin(request):
    #if request.user.is_authenticed:
    #    return redirect('login')
    #else:
    authForm = LoginForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request, 'Your username OR password is incorrect')

    return render(request, 'pages/login.html', {'form': authForm})


# ======================= LOGOUT
def userLogout(request):
    logout(request)
    return redirect('login')

# ======================= USER PROFILE
def userProfile(request):
    # if not request.user.is_authenticed():
    #     return redirect('login')
    # else:
    return render(request, 'pages/user_profile.html', {'user': request.user})


# ======================= PRODUCT LIST
def productList(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'pages/product_list.html', context)


# ======================= PRODUCT DETAILS
class ProductDetailView(DetailView):
    model = Product
    template_name = 'pages/product_details.html'

    def get_object(self):
        iProductId = self.kwargs['id']
        return {
            'product': Product.objects.get(id=iProductId),
            'gallery': ProductImage.objects.filter(product=iProductId)
        }


# ======================= SHOW CATEGORY
def showCategory(request, hierarchy=None):
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


# ======================= ADD TO CART
def addToCart(request, product_id):
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

    
# ======================= VIEW CART
def cartOverview(request):
    context = {
        'order' : Order.objects.filter(owner=request.user)
    }
    return render(request, 'pages/cart_overview.html', context)

def search_results(request):
    context = {}
    query = ""
    if request.GET:
        query = request.GET['q']
        context['query'] = str(query)

    context['products'] = query_search(query)

    return render(request, 'pages/search_results.html', context)


def query_search(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = Product.objects.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q)
        ).distinct()

        for post in posts:
            queryset.append(post)
    return list(set(queryset))