from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.list_products, name='list_products'),

    path('register/', views.register_user, name='register'),
    path('login/', views.user_login, name='login'),

    path('product', views.single_product, name='single_product')
]
