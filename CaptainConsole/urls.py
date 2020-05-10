from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.productList, name='list_products'),

    path('register/', views.registerUser, name='register'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.logout, name='logout'),

    path('product/<int:id>/<slug:slug>/', views.ProductDetailView.as_view(), name='product_details'),
    path('product/<int:id>/', views.ProductDetailView.as_view(), name='product_details')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
