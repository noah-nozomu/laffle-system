from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('order-complete/', views.order_complete, name='order_complete'),
    path('kitchen/', views.kitchen_monitor, name='kitchen_monitor'),
    
    # ★ここを追加
    path('qr/', views.qr_code_page, name='qr_code_page'),
]