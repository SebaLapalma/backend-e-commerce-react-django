# admin.py

from django.contrib import admin
from .models import Product, Review, Order, OrderItem, ShippingAddress

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'absolute_image_url', 'description', 'price', 'stock', 'createdAt')
    # ... otros ajustes según tus necesidades ...

    absolute_image_url.short_description = 'Absolute Image URL'

admin.site.register(Product, ProductAdmin)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
