from django.contrib import admin
from django.urls import path
from .views import list_products
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list', list_products, name='list_products'),

    path('register/', views.register_user, name='register'),
    path('login/', views.user_login, name='login')

]
