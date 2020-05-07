from django.contrib import admin
from django.urls import path
<<<<<<< HEAD

# the pages
from .views import list_products
from .views import single_product

urlpatterns = [
    path('', list_products, name="home_view"),  # renders page at root of website
    path('admin/', admin.site.urls),
    path('list', list_products, name='list_products'),
    path('product', single_product, name='single_product')
=======
from .views import list_products
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list', list_products, name='list_products'),

    path('register/', views.register_user, name='register'),
    path('login/', views.user_login, name='login')

>>>>>>> 3e0b78b91ef82263419fdb33f40f994646137cf5
]
