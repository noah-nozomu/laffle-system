from django.db import models
from django.utils import timezone

# 商品データ
class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="商品名")
    description = models.TextField(blank=True, null=True, verbose_name="説明")
    price = models.IntegerField(verbose_name="価格")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="商品画像")

    def __str__(self):
        return self.name

# 注文データ（レシート全体）
class Order(models.Model):
    created_at = models.DateTimeField(default=timezone.now, verbose_name="注文日時")
    total_price = models.IntegerField(default=0, verbose_name="合計金額")
    is_completed = models.BooleanField(default=False, verbose_name="提供済み")

    def __str__(self):
        return f"注文 #{self.id} - ¥{self.total_price}"

# 注文明細（レシートの各行）
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品")
    quantity = models.IntegerField(default=1, verbose_name="個数")
    price = models.IntegerField(verbose_name="購入時の価格")

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"