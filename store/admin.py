from django.contrib import admin
from .models import Product, Order, OrderItem

# 注文の中身（商品と個数）を、注文詳細ページの中に表示するための設定
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

# 注文管理画面の設定
class OrderAdmin(admin.ModelAdmin):
    # ★ここが重要：一覧画面に表示する項目
    # ID, 名前, 注文日時, 合計金額, 提供済みか を表示します
    list_display = ('id', 'customer_name', 'created_at', 'total_price', 'is_completed')
    
    # 右側に絞り込みフィルターを表示（提供済みか、日付で絞り込み可能）
    list_filter = ('is_completed', 'created_at')
    
    inlines = [OrderItemInline]

admin.site.register(Product)
admin.site.register(Order, OrderAdmin)