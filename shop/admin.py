from django.contrib import admin
from shop.models import *

# Register your models here.
admin.site.register((Category, Newsletter))

class ProductImageInline(admin.StackedInline):
    model = ProdImage

@admin.register(Product)
class PostAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__']

admin.site.register((Reviews))