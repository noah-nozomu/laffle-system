from django.urls import path
from . import views

urlpatterns = [
    # 1. メニュー一覧（トップページ）
    path('', views.product_list, name='product_list'),
    
    # 2. 商品の詳細画面
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    
    # 3. カートの中身を表示する画面
    path('cart/', views.cart_detail, name='cart_detail'),
    
    # 4. QRコード生成画面
    path('qr/', views.generate_qr, name='generate_qr'),
]