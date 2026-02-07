from django.db import models

class Category(models.Model):
    name = models.CharField("カテゴリ名", max_length=100)
    def __str__(self): return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="カテゴリ")
    name = models.CharField("商品名", max_length=100)
    price = models.IntegerField("価格")
    description = models.TextField("説明", blank=True, null=True)
    image = models.ImageField("商品画像", upload_to='products/', blank=True, null=True)
    def __str__(self): return self.name

# ★ここから下を追加しました！

class Order(models.Model):
    """注文全体（誰が、いつ）"""
    customer_name = models.CharField("お名前", max_length=100)
    created_at = models.DateTimeField("注文日時", auto_now_add=True)
    
# ★これを追加！「提供済みかどうか」を管理します
    is_served = models.BooleanField("提供済み", default=False)

    def __str__(self):
        return f"{self.customer_name} 様 ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

class OrderItem(models.Model):
    """注文の中身（どの商品を、何個）"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="注文ID")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品")
    quantity = models.PositiveIntegerField("個数")

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"