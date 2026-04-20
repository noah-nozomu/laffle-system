from django.db import models
from django.utils import timezone

# 商品データ
class Product(models.Model):
    # ★ここを追加：カテゴリの選択肢を作ります
    CATEGORY_CHOICES = (
        ('waffle', 'ワッフル'),
        ('drink', 'ドリンク'),
    )

    name = models.CharField(max_length=100, verbose_name="商品名")
    display_order = models.PositiveIntegerField(default=0, db_index=True, verbose_name="表示順")

    # ★ここを追加：商品ごとにカテゴリを選べるようにします
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='waffle', verbose_name="カテゴリ")

    TEMPERATURE_CHOICES = [
        ('none', '選択なし'),
        ('both', 'ホット・アイス'),
        ('hot',  'ホットのみ'),
        ('ice',  'アイスのみ'),
    ]
    temperature_option = models.CharField(
        max_length=10, choices=TEMPERATURE_CHOICES, default='none', verbose_name="温度オプション"
    )
    
    description = models.TextField(blank=True, null=True, verbose_name="説明")
    price = models.IntegerField(verbose_name="価格")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="商品画像")

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.name

# 注文データ（レシート全体）
class Order(models.Model):
    # ★ここにお客様の名前を追加しました
    customer_name = models.CharField(max_length=100, default="お客様", verbose_name="お名前")
    device_id = models.CharField(max_length=36, null=True, blank=True, verbose_name="デバイスID")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="注文日時")
    total_price = models.IntegerField(default=0, verbose_name="合計金額")
    is_completed = models.BooleanField(default=False, verbose_name="提供済み")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="提供完了日時")

    def __str__(self):
        # 管理画面などで見やすいように名前を表示します
        return f"{self.customer_name} 様 - ¥{self.total_price}"

# 注文明細（レシートの各行）
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品")
    quantity = models.IntegerField(default=1, verbose_name="個数")
    price = models.IntegerField(verbose_name="購入時の価格")
    temperature = models.CharField(max_length=5, blank=True, null=True, verbose_name="温度")

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"