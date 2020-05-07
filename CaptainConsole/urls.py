from django.contrib import admin
from django.urls import path

# the pages
from .views import list_products
from .views import single_product

urlpatterns = [
    path('', list_products, name="home_view"),  # renders page at root of website
    path('admin/', admin.site.urls),
    path('list', list_products, name='list_products'),
    path('product', single_product, name='single_product')
]
