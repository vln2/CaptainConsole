from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.productList, name='home'),


    path('search_results/', views.search_results, name='search_results'),

    path('register/', views.registerUser, name='register'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),

    path('profile/', views.userProfile, name="user_profile"),

    path('product/<int:id>/<slug:slug>/', views.ProductDetailView.as_view(), name='product_details_slug'),
    path('product/<int:id>/', views.ProductDetailView.as_view(), name='product_details'),

    path('add-to-cart/<int:product_id>', views.addToCart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>', views.addToCart, name='remove_from_cart'),

    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

    path('category/', views.productList, name='category'),
    re_path(r'^category/(?P<hierarchy>.+)/$', views.showCategory, name='category_tree'),

    # catch all
    re_path(r'^.*/$', views.notFound, name="not_found")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
