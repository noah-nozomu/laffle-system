from django.urls import path
from . import views

urlpatterns = [
    # お客さん用ページ
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.order_success, name='order_success'),
    
    # 店長用ページ（QRコード作成）
    path('qr/', views.generate_qr, name='generate_qr'),
    
    # ★ここが新機能（ダッシュボードへの入り口）
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # ★ここが新機能（注文を「完了」にするための裏口）
    path('dashboard/complete/<int:order_id>/', views.complete_order, name='complete_order'),
]