from django.contrib import admin

from .models import Product, UserInfo

admin.site.register(Product)
admin.site.register(UserInfo)
