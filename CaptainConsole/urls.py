from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.listProducts, name='list_products'),

    path('register/', views.registerUser, name='register'),
    path('login/', views.userLogin, name='login'),

    path('products/<slug:slug>', views.ProductDetailView.as_view(), name='product_details')

]
