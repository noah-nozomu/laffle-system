from django.urls import path
from . import views

urlpatterns = [
    # お客さん用ページ
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    
    # カート機能（追加・見る・更新・削除）
    path('add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),   # ★追加：個数変更用
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'), # ★追加：削除用
    
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.order_success, name='order_success'),
    
    # 店長用ページ（QRコード作成）
    path('qr/', views.generate_qr, name='generate_qr'),
    
    # ダッシュボード（売上・キッチンモニター）
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # 注文を「完了」にする機能
    path('dashboard/complete/<int:order_id>/', views.complete_order, name='complete_order'),
]