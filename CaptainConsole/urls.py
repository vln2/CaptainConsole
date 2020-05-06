from django.contrib import admin
from django.urls import path
from .views import list_products

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list', list_products, name='list_products')
]
