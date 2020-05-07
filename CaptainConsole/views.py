from django.shortcuts import render
from .models import Product


def list_products(request):
    # context = {
    #     'products': Product.objects.all()
    # }
    return render(request, 'catalog/list_products.html')


def single_product(request):

    # context = {
    #     'product': Product.objects.all()
    # }
    return render(request, 'product/single_product.html')
