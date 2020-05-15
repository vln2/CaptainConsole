from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from .models import Product, Category, ProductImage, Order, Item, Shipping, UserInfo
from .forms import CreatingUserForms, AddItemToCartForm, LoginForm, AddressForm, PaymentForm, RemoveItemFromCartForm
from django.db.models import Q
from django.http import Http404, HttpResponseBadRequest

#just strings for checking for sorting options 
VALID_SORTS = {
    'price_asc': 'price',
    'price_desc': '-price',
    'name_asc': 'name',
    'name_desc': '-name'
}

PRODUCTS_PER_PAGE = 12

# ======================= SALES / FRONT PAGE

def currentSales(request):
    #get all products that are on sale
    products = Product.objects.all() #Product.objects.filter('discount' > 0)
    
    context = {
        'products':products
    }
    return render(request, 'pages/sales.html', context)
# ======================= REGISTER USER
def registerUser(request):
    #if request.user.is_authenticed:
    #    return redirect('base')
    registerForm = CreatingUserForms()
    #else:
    if request.method == 'POST':
        registerForm = CreatingUserForms(request.POST)
        if registerForm.is_valid():
            user = registerForm.save()
            userInfo = UserInfo.objects.create(user=user)
            messages.success(request, 'Account has been made, Welcome ' + user.username)
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

# ======================= FORGOT PASSWORD
def forgot_password(request):
    if request.method == 'POST':
        return password_reset(request, from_email=request.POST.get('email'))
    else:
        return render(request, 'forgot_password_form.html')

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
    products = Product.objects.all()
    #if the user wishes to sort by name/price

    query = request.GET.get('sort_by')
    if query:
        if query in VALID_SORTS:
            products = Product.objects.all().order_by(VALID_SORTS[query])
  
    

    #sort products into pages
    paginator = Paginator(products, PRODUCTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
            
    context = {
        'products': page_obj
    }

    return render(request, 'pages/product_list.html', context)


# ======================= PRODUCT DETAILS
class ProductDetailView(DetailView):
    model = Product
    template_name = 'pages/product_details.html'

    def get_object(self):
        try:
            iProductId = self.kwargs['id']
            return {
                'add_to_cart_form': AddItemToCartForm,
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
        paginator = Paginator(products, PRODUCTS_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'add_to_cart_form': AddItemToCartForm,
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
    userInfo = get_object_or_404(UserInfo, user=request.user)
    form = AddItemToCartForm(request.POST or None)

    if form.is_valid():
        if not isinstance(userInfo.cart, Order):
            userInfo.cart = Order.objects.create(owner=request.user, status=Order.CART)
            userInfo.save()

        item = Item.objects.get_or_create(order=userInfo.cart, product=product)
        if item[1]:
            item[0].save()
            messages.info(request, "This item was added to your cart.")
        else:
            item[0].quantity += form.cleaned_data.get('quantity')
            item[0].save()
            messages.info(request, "This item:{item[0]} quantity was updated.")

    try:
        httpheaders = request.headers
        refer = httpheaders['Referer']
    except:
        return HttpResponseBadRequest('Bad Request')
    return redirect(refer)


def removeFromCart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    userInfo = get_object_or_404(UserInfo, user=request.user)
    form = RemoveItemFromCartForm(request.POST or None)
    try:
        httpheaders = request.headers
        refer = httpheaders['Referer']
    except:
        return HttpResponseBadRequest('Bad Request')

    if form.is_valid():
        if not isinstance(userInfo.cart, Order):
            messages.error(request, "User has no cart")
            return redirect(refer)

        item = Item.objects.get(order=userInfo.cart, product=product)
        if isinstance(item, Item):
            item.quantity -= form.cleaned_data.get('quantity')
            if item.quantity < 1:
                item.delete()
            else:
                item.save()
            messages.info(request, "Item removed from cart")
        else:
            messages.info(request, f"No item {product} was found in {request.user} cart")

    return redirect(refer)


# ======================= VIEW CART
def cart(request):
    userInfo = get_object_or_404(UserInfo, user=request.user)
    if not isinstance(userInfo.cart, Order):
        userInfo.cart = Order.objects.create(owner=request.user, status=Order.CART)
        userInfo.save()

    class breadcrumb:
        get_slug_link = reverse('cart')
        def __str__(self):
            return 'Cart'

    items = userInfo.cart.getItems
    context = {
        'removeitem': RemoveItemFromCartForm(),
        'cart': userInfo.cart,
        'items': items,
        'breadcrumbs': (breadcrumb,)
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
