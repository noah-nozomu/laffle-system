from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path
from store import views as store_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),

    # デモ用URL（DBに保存しない）
    path('demo/', store_views.demo_category_list, name='demo_category_list'),
    path('demo/menu/<str:category_name>/', store_views.demo_product_list, name='demo_product_list'),
    path('demo/product/<int:pk>/', store_views.product_detail, name='demo_product_detail'),
    path('demo/add/<int:pk>/', store_views.demo_add_to_cart, name='demo_add_to_cart'),
    path('demo/cart/', store_views.demo_cart_detail, name='demo_cart_detail'),
    path('demo/cart/update/<int:product_id>/', store_views.demo_update_cart, name='demo_update_cart'),
    path('demo/cart/remove/<int:product_id>/', store_views.demo_remove_from_cart, name='demo_remove_from_cart'),
    path('demo/checkout/', store_views.checkout_demo, name='demo_checkout'),
    path('demo/success/', store_views.demo_order_success, name='demo_order_success'),

    # メディアファイル（写真）を強制的に表示する設定
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]