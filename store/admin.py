from django.contrib import admin
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import path, reverse
from django.utils.html import format_html
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

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'temperature_option', 'display_order', 'move_buttons')
    list_editable = ('temperature_option',)
    list_filter = ('category', 'temperature_option')
    ordering = ('display_order', 'id')
    actions = ('move_selected_up', 'move_selected_down')

    @admin.display(description='並び順変更')
    def move_buttons(self, obj):
        move_up_url = reverse('admin:store_product_move', args=[obj.pk, 'up'])
        move_down_url = reverse('admin:store_product_move', args=[obj.pk, 'down'])
        return format_html(
            '<a class="button" href="{}">↑ 上へ</a>&nbsp;<a class="button" href="{}">↓ 下へ</a>',
            move_up_url,
            move_down_url,
        )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:product_id>/move/<str:direction>/',
                self.admin_site.admin_view(self.move_product),
                name='store_product_move',
            ),
        ]
        return custom_urls + urls

    def _resequence(self, ordered_ids):
        with transaction.atomic():
            for index, product_id in enumerate(ordered_ids, start=1):
                Product.objects.filter(id=product_id).update(display_order=index)

    def _move_ids(self, selected_ids, direction):
        ordered_ids = list(Product.objects.order_by('display_order', 'id').values_list('id', flat=True))
        selected_set = set(selected_ids)
        original_ids = ordered_ids.copy()

        if direction == 'up':
            for idx in range(1, len(ordered_ids)):
                if ordered_ids[idx] in selected_set and ordered_ids[idx - 1] not in selected_set:
                    ordered_ids[idx - 1], ordered_ids[idx] = ordered_ids[idx], ordered_ids[idx - 1]
        else:
            for idx in range(len(ordered_ids) - 2, -1, -1):
                if ordered_ids[idx] in selected_set and ordered_ids[idx + 1] not in selected_set:
                    ordered_ids[idx], ordered_ids[idx + 1] = ordered_ids[idx + 1], ordered_ids[idx]

        moved = ordered_ids != original_ids
        if moved:
            self._resequence(ordered_ids)
        return moved

    def move_product(self, request, product_id, direction):
        if direction not in ('up', 'down'):
            self.message_user(request, '不正な操作です。', level=messages.ERROR)
            return redirect('admin:store_product_changelist')

        product = get_object_or_404(Product, pk=product_id)
        moved = self._move_ids([product.id], direction)

        if moved:
            self.message_user(request, f'「{product.name}」の表示順を更新しました。')
        else:
            self.message_user(request, 'これ以上移動できません。', level=messages.WARNING)

        return redirect('admin:store_product_changelist')

    @admin.action(description='選択した商品を1つ上へ移動')
    def move_selected_up(self, request, queryset):
        moved = self._move_ids(queryset.values_list('id', flat=True), 'up')
        if moved:
            self.message_user(request, '選択した商品の表示順を上へ移動しました。')
        else:
            self.message_user(request, 'これ以上上へ移動できません。', level=messages.WARNING)

    @admin.action(description='選択した商品を1つ下へ移動')
    def move_selected_down(self, request, queryset):
        moved = self._move_ids(queryset.values_list('id', flat=True), 'down')
        if moved:
            self.message_user(request, '選択した商品の表示順を下へ移動しました。')
        else:
            self.message_user(request, 'これ以上下へ移動できません。', level=messages.WARNING)

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)