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
        products = Product.objects.filter(category=category_name)
    else:
        products = Product.objects.all()
        
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
    cart = request.session.get('cart', {})
    product_id = str(pk)
    
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity
    
    request.session['cart'] = cart
    return redirect('cart_detail')

# 4. カートを見る
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            subtotal = product.price * quantity
            total_price += subtotal
            cart_items.append({
                'product': product, 
                'quantity': quantity, 
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
        
        str_id = str(product_id)
        if str_id in cart:
            if new_quantity > 0:
                cart[str_id] = new_quantity
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
        name = request.POST.get('customer_name', 'お客様')
        order = Order.objects.create(total_price=0, customer_name=name)
        
        total = 0
        for product_id, quantity in cart.items():
            try:
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )
                total += product.price * quantity
            except Product.DoesNotExist:
                continue
        
        order.total_price = total
        order.save()
        
        request.session['cart'] = {} 
        
        return render(request, 'store/order_success.html')
    
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