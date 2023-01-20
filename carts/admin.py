from django.contrib import admin
from .models import Cart,Cartitem


class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'date_added']
class CartitemAdmin(admin.ModelAdmin):
    list_display = ['product', 'carts','quantity', 'is_active']
# Register your models here.

admin.site.register(Cart,CartAdmin)
admin.site.register(Cartitem,CartitemAdmin)


