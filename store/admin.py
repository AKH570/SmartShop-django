from django.contrib import admin
from .models import Product
# Register your models here.


class ProductAccount(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'stock', 'category', 'modified_date']
    prepopulated_fields = {'slug': ('product_name',)}


admin.site.register(Product, ProductAccount)