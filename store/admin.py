from django.contrib import admin
from .models import Product, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'total_price', 'is_completed')
    inlines = [OrderItemInline]

admin.site.register(Product)
admin.site.register(Order, OrderAdmin)