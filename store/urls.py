from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('checkout/', views.checkout, name='checkout'),  # 注文確定ボタン
    path('success/', views.order_success, name='order_success'), # 完了画面
    path('qr/', views.generate_qr, name='generate_qr'),
]