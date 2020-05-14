from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'thumb')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        ProductImageInline,
    ]

# class ProductInline(admin.TabularInline):
#     model = Product


class CategoryAdmin(MPTTModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)
admin.site.register(UserInfo)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order)
admin.site.register(Item)
admin.site.register(Payment)
admin.site.register(Shipping)
admin.site.register(Address)