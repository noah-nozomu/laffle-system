from django.contrib import admin
from .models import Category, Product, Order, OrderItem

# 注文の中身を、注文詳細画面の中に表示するための設定
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('customer_name', 'created_at') # 一覧にお名前と日時を表示

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
# OrderItemはOrderの中に表示するので、個別登録は不要