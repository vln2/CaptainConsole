from django.contrib import admin

from .models import Product, UserInfo, Category

admin.site.register(Product)
admin.site.register(UserInfo)
admin.site.register(Category)
