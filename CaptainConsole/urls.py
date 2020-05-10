from django.contrib import admin
from django.urls import path, re_path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.productList, name='list_products'),

    path('register/', views.registerUser, name='register'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.logout, name='logoin'),

    path('products/<slug:slug>', views.ProductDetailView.as_view(), name='product_details'),

    re_path(r'^category/(?P<hierarchy>.+)/$', views.show_category, name='category'),
]
