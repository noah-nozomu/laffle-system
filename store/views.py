import qrcode
import base64
from io import BytesIO
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem

# 商品一覧
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

# 商品詳細
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

# カートに追加
def add_to_cart(request, pk):
    quantity = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        cart[str(pk)] += quantity
    else:
        cart[str(pk)] = quantity
    request.session['cart'] = cart
    return redirect('cart_detail')

# カートを見る
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total_price += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
    return render(request, 'store/cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})

# 注文確定（ここが新機能！）
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('product_list')

    # 注文を作成
    order = Order.objects.create(total_price=0)
    
    total = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )
        total += product.price * quantity
    
    # 合計金額を保存してカートを空にする
    order.total_price = total
    order.save()
    request.session['cart'] = {} 
    
    return redirect('order_success')

# 注文完了画面
def order_success(request):
    return render(request, 'store/order_success.html')

# QRコード
def generate_qr(request):
    url = "https://laffle.onrender.com"
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    return render(request, 'store/qr_code.html', {'qr_code': qr_code_base64, 'url': url})