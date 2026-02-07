from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Product, Order, OrderItem
import socket
import qrcode
import io
import base64

def get_ip_address():
    """自分のPCのIPアドレス（住所）を調べる"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # GoogleのDNSに繋ぐフリをして自分のIPを特定する
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

# --- ここから下は既存の機能 ---

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        quantity = int(request.POST.get('quantity', 1))
        product_id = str(pk)
        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity
        request.session['cart'] = cart
        return redirect('cart_detail')
    return render(request, 'store/product_detail.html', {'product': product})

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(pk=product_id)
            subtotal = product.price * quantity
            total_price += subtotal
            cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        except Product.DoesNotExist:
            continue
    return render(request, 'store/cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})

def order_complete(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        customer_name = request.POST.get('customer_name')
        if cart and customer_name:
            order = Order.objects.create(customer_name=customer_name)
            for product_id, quantity in cart.items():
                try:
                    product = Product.objects.get(pk=product_id)
                    OrderItem.objects.create(order=order, product=product, quantity=quantity)
                except Product.DoesNotExist:
                    continue
            del request.session['cart']
            return render(request, 'store/order_complete.html', {'customer_name': customer_name})
    return redirect('product_list')

def kitchen_monitor(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        if order_id:
            order = get_object_or_404(Order, pk=order_id)
            order.is_served = True
            order.save()
        return redirect('kitchen_monitor')
    orders = Order.objects.filter(is_served=False).order_by('created_at')
    return render(request, 'store/kitchen_monitor.html', {'orders': orders})

# --- ★新機能：QRコード表示 ---

def qr_code_page(request):
    """注文画面へのQRコードを生成して表示する"""
    ip = "172.16.0.35"
    # スマホがアクセスすべきURL（例：http://192.168.1.5:8000/）
    url = f"http://{ip}:8000/"
    
    # QRコードを作成
    img = qrcode.make(url)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return render(request, 'store/qr_code.html', {'qr_image': img_str, 'url': url})