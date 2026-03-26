from django.urls import path
from . import views

urlpatterns = [
    path('', views.demo_category_list, name='demo_category_list'),
    path('menu/<str:category_name>/', views.demo_product_list, name='demo_product_list'),
    path('add/<int:pk>/', views.demo_add_to_cart, name='demo_add_to_cart'),
    path('cart/', views.demo_cart_detail, name='demo_cart_detail'),
    path('cart/update/<int:product_id>/', views.demo_update_cart, name='demo_update_cart'),
    path('cart/remove/<int:product_id>/', views.demo_remove_from_cart, name='demo_remove_from_cart'),
    path('checkout/', views.checkout_demo, name='demo_checkout'),
]
