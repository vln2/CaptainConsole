from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from .models import Product, Category, ProductImage, Order, Item, Shipping
from .forms import CreatingUserForms, AddItemToCartForm, LoginForm, AddressForm, PaymentForm
from django.db.models import Q
from django.http import Http404

#just strings for checking for sorting options 
VALID_SORTS = {
    'price_asc': 'price',
    'price_desc': '-price',
    'name_asc': 'name',
    'name_desc': '-name'
}

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
    return HttpResponseRedirect('/')

# ======================= USER PROFILE
def userProfile(request):
    # if not request.user.is_authenticed():
    #     return redirect('login')
    # else:
    return render(request, 'pages/user_profile.html', {'user': request.user})


# ======================= PRODUCT LIST
def productList(request, *args):
    context = {
        'products': Product.objects.all()
    }

    #if the user wishes to sort by name/price
    query = request.GET.get('sort_by')
    if query:
        if query in VALID_SORTS:
            context['products'] = Product.objects.all().order_by(VALID_SORTS[query])
    
            
            
    return render(request, 'pages/product_list.html', context)


# ======================= PRODUCT DETAILS
class ProductDetailView(DetailView):
    model = Product
    template_name = 'pages/product_details.html'

    def get_object(self):
        try:
            iProductId = self.kwargs['id']
            return {
                'product': Product.objects.get(id=iProductId),
                'gallery': ProductImage.objects.filter(product=iProductId)
            }
        except Product.DoesNotExist:
            raise Http404("Product does not exist")



# ======================= SHOW CATEGORY
def showCategory(request, hierarchy=None):
    try:
        categories_slug = hierarchy.split('/')
        category_slug = categories_slug[-1]
        category = Category.objects.get(slug=category_slug)

        products = category.get_products()

        # if user wishes to sort the list by name/price
        query = request.GET.get('sort_by')
        if query:
            if query in VALID_SORTS:
                products = category.get_products(sort_by=VALID_SORTS[query])

        #sort products into pages
        paginator = Paginator(products, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'add_to_cart_form': AddItemToCartForm(),
            'instance': category,
            'products': page_obj,
            'breadcrumbs': category.get_ancestors(include_self=True)
        }

    except Category.DoesNotExist:
        raise Http404("Category not found")

    return render(request, 'pages/product_list.html', context)


# ======================= ADD TO CART
def addToCart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = AddItemToCartForm(request.POST or None)
    if form.is_valid():

        order_qs = Order.objects.filter(owner=request.user, status=Order.CART)
        if order_qs.exists():
            order = order_qs.first()
        else:
            order = Order.objects.create(owner=request.user, status=Order.CART)

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
def cart(request):
    order_qs = Order.objects.filter(owner=request.user, status=Order.CART)
    if order_qs.exists():
        cart = order_qs.first()
    else:
        cart = Order.objects.create(owner=request.user, status=Order.CART)

    context = {
        'cart': cart
    }
    return render(request, 'pages/cart.html', context)


def checkout(request, order_id):
    order_qs = Order.objects.filter(owner=request.user, status=Order.CART, id=order_id)
    if order_qs.exists():
        order = order_qs.first()
    else:
        messages.error(request, f'No order with id:{order_id} found')
        return redirect('home')

    addressform = AddressForm(request.POST or None, prefix='address')
    paymentform = PaymentForm(request.POST or None, prefix='payment')

    if request.method == 'POST':

        if addressform.is_valid() and paymentform.is_valid():
            new_address = addressform.save()
            new_payment = paymentform.save()

            order.status = Order.PAYMENT
            order.shipping = Shipping.objects.create(address=new_address)
            order.payment = new_payment
            order.save()

            return redirect('review', order_id=order_id)

    context = {
        'addressform': addressform,
        'paymentform': paymentform,
        'cart': order
    }
    return render(request, 'pages/checkout.html', context)


def order_review(request, order_id):
    order_qs = Order.objects.filter(owner=request.user, id=order_id)
    if order_qs.exists():
        order = order_qs.first()
    else:
        messages.error(request, f'No order with id:{order_id} found')
        return redirect('home')

    context = {
        'order': order,
        'cart': order.items.all(),
        'address': order.shipping.address,
        'payment': order.payment,
    }
    return render(request, 'pages/order_review.html', context)


# ======================= SEARCH RESULTS
def search_results(request):
    context = {}
    query = ""
    if request.GET:
        query = request.GET['q']
        context['query'] = str(query)

    context['products'] = query_search(query)

    return render(request, 'pages/search_results.html', context)


# ======================= SEARCH QUERY
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
    
# ======================= SEARCH QUERY
def notFound(request):
    raise Http404("Page not found")
