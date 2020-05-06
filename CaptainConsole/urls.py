from django.contrib import admin
from django.urls import path

# the pages
from pages.views import home_view
from pages.views import list_products

urlpatterns = [
    path('', home_view, name="home_view"),  # renders page at root of website
    path('admin/', admin.site.urls),
    path('list', list_products, name='list_products'),
]
