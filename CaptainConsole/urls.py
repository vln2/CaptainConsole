from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    # == Home
    path('', views.productList, name='home'),

    # == Authentication
    path('admin/', admin.site.urls),
    path('register/', views.registerUser, name='register'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),

    # == UserProfile
    path('profile/', views.userProfile, name="user_profile"),

    # == Forgot password
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^reset/(?P<hierarchy>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_complete'),
    re_path(r'^reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_complete'),

    # == Catalog and Categories
    path('catalog/', views.productList, name='catalog'),
    path('category/', views.productList, name='category'),
    re_path(r'^category/(?P<hierarchy>.+)/$', views.showCategory, name='category_tree'),

    # == Single product
    path('product/<int:id>/<slug:slug>/', views.ProductDetailView.as_view(), name='product_details_slug'),
    path('product/<int:id>/', views.ProductDetailView.as_view(), name='product_details'),

    # == Search
    path('search_results/', views.search_results, name='search_results'),

    # == Cart
    path('cart/', views.cart, name="cart"),
    path('add-to-cart/<int:product_id>', views.addToCart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>', views.removeFromCart, name='remove_from_cart'),

    # == Checkout
    path('cart/', views.cart, name="cart"),
    path('checkout/<int:order_id>', views.checkout, name="checkout"),
    path('review/<int:order_id>', views.order_review, name="review"),

    # == catch all
    re_path(r'^.*/$', views.notFound, name="not_found")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
