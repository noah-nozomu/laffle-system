import uuid
import qrcode
import base64
from io import BytesIO
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Sum
from .models import Product, Order, OrderItem

# ==========================================
# ★ここから変更・追加した部分
# ==========================================

# ★新規追加：トップページ（ワッフルかドリンクを選ぶ画面）
def category_list(request):
    return render(request, 'store/category_list.html')

# ★変更：メニュー一覧（選ばれたカテゴリだけで絞り込む）
def product_list(request, category_name=None):
    if category_name:
        products = Product.objects.filter(category=category_name).order_by('display_order', 'id')
    else:
        products = Product.objects.all().order_by('display_order', 'id')
        
    return render(request, 'store/product_list.html', {
        'products': products,
        'category_name': category_name
    })

# ==========================================
# ★ここからは今までと【全く同じ】です！（一切いじっていません）
# ==========================================

# 2. 商品詳細
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

# 3. カートに追加
def add_to_cart(request, pk):
    quantity = int(request.POST.get('quantity', 1))
    temperature = request.POST.get('temperature', '')
    cart = request.session.get('cart', {})
    product_id = str(pk)

    if product_id in cart:
        existing = cart[product_id]
        if isinstance(existing, dict):
            existing['quantity'] += quantity
            if temperature:
                existing['temperature'] = temperature
        else:
            cart[product_id] = {'quantity': existing + quantity, 'temperature': temperature}
    else:
        cart[product_id] = {'quantity': quantity, 'temperature': temperature}

    request.session['cart'] = cart
    return redirect('cart_detail')

# 4. カートを見る
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            if isinstance(item_data, dict):
                quantity = item_data.get('quantity', 1)
                temperature = item_data.get('temperature', '')
            else:
                quantity = item_data
                temperature = ''
            subtotal = product.price * quantity
            total_price += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'temperature': temperature,
                'subtotal': subtotal
            })
        except Product.DoesNotExist:
            continue

    return render(request, 'store/cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

# カート内の数量変更（0以下なら削除）
def update_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        new_quantity = int(request.POST.get('quantity', 1))

        temperature = request.POST.get('temperature', '')
        str_id = str(product_id)
        if str_id in cart:
            if new_quantity > 0:
                existing = cart[str_id]
                if isinstance(existing, dict):
                    existing['quantity'] = new_quantity
                    if temperature:
                        existing['temperature'] = temperature
                else:
                    cart[str_id] = {'quantity': new_quantity, 'temperature': temperature}
            else:
                del cart[str_id]

        request.session['cart'] = cart
    return redirect('cart_detail')

# カートから商品を削除
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    str_id = str(product_id)
    
    if str_id in cart:
        del cart[str_id]
        request.session['cart'] = cart
        
    return redirect('cart_detail')

# 5. 注文確定（名前も保存）
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        # ★ここだけ変更：カートが空なら「カテゴリ選択画面」に戻す
        return redirect('category_list')

    if request.method == 'POST':
        from django.conf import settings
        if getattr(settings, 'DEMO_MODE', False):
            request.session['cart'] = {}
            return render(request, 'store/order_success_demo.html')
        name = request.POST.get('customer_name', 'お客様')

        # デバイスIDをクッキーから取得、なければ新規生成
        device_id = request.COOKIES.get('device_id') or str(uuid.uuid4())

        # 同じdevice_id＋同じ名前の未完了注文を探す
        existing_order = Order.objects.filter(
            device_id=device_id,
            customer_name=name,
            is_completed=False
        ).first()

        if existing_order:
            order = existing_order
        else:
            order = Order.objects.create(total_price=0, customer_name=name, device_id=device_id)

        for product_id, item_data in cart.items():
            try:
                product = Product.objects.get(id=product_id)
                if isinstance(item_data, dict):
                    quantity = item_data.get('quantity', 1)
                    temperature = item_data.get('temperature', '') or None
                else:
                    quantity = item_data
                    temperature = None
                existing_item = order.items.filter(product=product).first()
                if existing_item:
                    existing_item.quantity += quantity
                    existing_item.save()
                else:
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=product.price,
                        temperature=temperature,
                    )
            except Product.DoesNotExist:
                continue

        order.total_price = sum(i.price * i.quantity for i in order.items.all())
        order.save()

        request.session['cart'] = {}

        response = render(request, 'store/order_success.html')
        response.set_cookie('device_id', device_id, max_age=60 * 60 * 24 * 365)
        return response
    
    return redirect('cart_detail')

# 6. 完了画面
def order_success(request):
    return render(request, 'store/order_success.html')

# 7. QRコード生成
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

# 8. ダッシュボード（売上とキッチンモニター）
def dashboard(request):
    active_orders = Order.objects.filter(is_completed=False).order_by('created_at')
    today = timezone.now().date()
    todays_orders = Order.objects.filter(created_at__date=today)
    total_sales = todays_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
    item_stats = OrderItem.objects.filter(order__created_at__date=today)\
        .values('product__name')\
        .annotate(total_qty=Sum('quantity'))\
        .order_by('-total_qty')

    return render(request, 'store/dashboard.html', {
        'active_orders': active_orders,
        'total_sales': total_sales,
        'item_stats': item_stats,
    })

# 9. 注文完了処理（提供済みボタン用）
def complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.is_completed = True
    order.save()
    return redirect('dashboard')

# 10. 注文削除
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
    return redirect('dashboard')

# 11. 注文編集（数量変更・商品削除）
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        for item in order.items.all():
            qty_key = f'quantity_{item.id}'
            delete_key = f'delete_{item.id}'
            if delete_key in request.POST:
                item.delete()
            else:
                new_qty = int(request.POST.get(qty_key, item.quantity))
                if new_qty > 0:
                    item.quantity = new_qty
                    item.save()
                else:
                    item.delete()
        # 明細が全削除されたら注文ごと削除、そうでなければ合計を再計算
        if order.items.exists():
            order.total_price = sum(i.price * i.quantity for i in order.items.all())
            order.save()
        else:
            order.delete()
        return redirect('dashboard')
    products = Product.objects.all().order_by('display_order', 'id')
    return render(request, 'store/edit_order.html', {'order': order, 'products': products})

# 12. 編集画面から商品を追加
def add_item_to_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)

        existing = order.items.filter(product=product).first()
        if existing:
            existing.quantity += quantity
            existing.save()
        else:
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)

        order.total_price = sum(i.price * i.quantity for i in order.items.all())
        order.save()

    return redirect('edit_order', order_id=order_id)


# ==========================================
# デモ用ビュー（DBに保存しない）
# ==========================================

def demo_category_list(request):
    return render(request, 'store/demo_category_list.html')


def demo_product_list(request, category_name=None):
    if category_name:
        products = Product.objects.filter(category=category_name).order_by('display_order', 'id')
    else:
        products = Product.objects.all().order_by('display_order', 'id')
    return render(request, 'store/demo_product_list.html', {
        'products': products,
        'category_name': category_name,
    })


def demo_add_to_cart(request, pk):
    quantity = int(request.POST.get('quantity', 1))
    temperature = request.POST.get('temperature', '')
    cart = request.session.get('demo_cart', {})
    product_id = str(pk)

    if product_id in cart:
        existing = cart[product_id]
        if isinstance(existing, dict):
            existing['quantity'] += quantity
            if temperature:
                existing['temperature'] = temperature
        else:
            cart[product_id] = {'quantity': existing + quantity, 'temperature': temperature}
    else:
        cart[product_id] = {'quantity': quantity, 'temperature': temperature}

    request.session['demo_cart'] = cart
    return redirect('demo_cart_detail')


def demo_cart_detail(request):
    cart = request.session.get('demo_cart', {})
    cart_items = []
    total_price = 0

    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            if isinstance(item_data, dict):
                quantity = item_data.get('quantity', 1)
                temperature = item_data.get('temperature', '')
            else:
                quantity = item_data
                temperature = ''
            subtotal = product.price * quantity
            total_price += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'temperature': temperature,
                'subtotal': subtotal,
            })
        except Product.DoesNotExist:
            continue

    return render(request, 'store/demo_cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


def demo_update_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('demo_cart', {})
        new_quantity = int(request.POST.get('quantity', 1))
        temperature = request.POST.get('temperature', '')
        str_id = str(product_id)
        if str_id in cart:
            if new_quantity > 0:
                existing = cart[str_id]
                if isinstance(existing, dict):
                    existing['quantity'] = new_quantity
                    if temperature:
                        existing['temperature'] = temperature
                else:
                    cart[str_id] = {'quantity': new_quantity, 'temperature': temperature}
            else:
                del cart[str_id]
        request.session['demo_cart'] = cart
    return redirect('demo_cart_detail')


def demo_remove_from_cart(request, product_id):
    cart = request.session.get('demo_cart', {})
    str_id = str(product_id)
    if str_id in cart:
        del cart[str_id]
        request.session['demo_cart'] = cart
    return redirect('demo_cart_detail')


def checkout_demo(request):
    cart = request.session.get('demo_cart', {})
    if not cart:
        return redirect('demo_category_list')
    if request.method == 'POST':
        request.session['demo_cart'] = {}
        return render(request, 'store/order_success_demo.html')
    return redirect('demo_cart_detail')


def demo_order_success(request):
    return render(request, 'store/order_success_demo.html')