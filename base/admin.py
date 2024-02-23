# admin.py

from django.contrib import admin
from .models import Product, Review, Order, OrderItem, ShippingAddress

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'stock', 'createdAt')
    # ... otros ajustes según tus necesidades ...

admin.site.register(Product, ProductAdmin)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
