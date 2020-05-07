from django.contrib import admin

from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}


class ProductInline(admin.TabularInline):
    model = Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    inlines = [ProductInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(UserInfo)
admin.site.register(Category, CategoryAdmin)
