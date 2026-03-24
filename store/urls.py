from django.urls import path
from . import views

urlpatterns = [
    # ==========================================
    # ★ここが変更点！（入り口を分けました）
    # ==========================================
    path('', views.category_list, name='category_list'), # 最初の画面（カテゴリ選択）
    path('menu/<str:category_name>/', views.product_list, name='product_list'), # 選んだカテゴリのメニュー一覧
    
    # ==========================================
    # ★ここから下は今までと【全く同じ】です！
    # ==========================================
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    
    # カート機能（追加・見る・更新・削除）
    path('add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.order_success, name='order_success'),
    
    # 店長用ページ（QRコード作成）
    path('qr/', views.generate_qr, name='generate_qr'),
    
    # ダッシュボード（売上・キッチンモニター）
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # 注文を「完了」にする機能
    path('dashboard/complete/<int:order_id>/', views.complete_order, name='complete_order'),

    # 注文の削除・編集
    path('dashboard/delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('dashboard/edit/<int:order_id>/', views.edit_order, name='edit_order'),
    path('dashboard/order/<int:order_id>/add-item/', views.add_item_to_order, name='add_item_to_order'),
]