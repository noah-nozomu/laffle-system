import qrcode
import base64
from io import BytesIO
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Sum
from .models import Product, Order, OrderItem

# 1. メニュー一覧
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

# 2. 商品詳細
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

# 3. カートに追加
def add_to_cart(request, pk):
    # フォームから送られてきた数量を取得（デフォルトは1）
    quantity = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})
    
    # IDを文字列にして保存（セッションのキーは文字列である必要があるため）
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
        # 商品が存在しない場合のエラー回避
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

# ★追加機能 1：カート内の数量変更（0以下なら削除）
def update_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        # 入力された新しい数量を取得
        new_quantity = int(request.POST.get('quantity', 1))
        
        str_id = str(product_id)
        if str_id in cart:
            if new_quantity > 0:
                cart[str_id] = new_quantity
            else:
                del cart[str_id]  # 0以下なら削除
            
        request.session['cart'] = cart
    return redirect('cart_detail')

# ★追加機能 2：カートから商品を削除
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
        return redirect('product_list')

    # POSTリクエスト（注文ボタンが押されたとき）だけ処理する
    if request.method == 'POST':
        # フォームから名前を受け取る（入力がなければ「お客様」にする）
        name = request.POST.get('customer_name', 'お客様')
        
        # 名前付きで注文を作成
        # 一旦合計金額0で作り、後で計算して更新する
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
        
        # カートを空にする
        request.session['cart'] = {} 
        
        return render(request, 'store/order_success.html')
    
    # もしURLを直接叩かれた場合などはカートに戻す
    return redirect('cart_detail')

# 6. 完了画面（リダイレクトではなく直接renderで表示する場合もあるが、URLを分けたい場合はここ）
def order_success(request):
    return render(request, 'store/order_success.html')

# 7. QRコード生成
def generate_qr(request):
    # 本番環境のURL
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
    # 未提供の注文を取得（古い順）
    active_orders = Order.objects.filter(is_completed=False).order_by('created_at')

    # 今日の日付を取得
    today = timezone.now().date()
    
    # 今日の注文だけを取得
    todays_orders = Order.objects.filter(created_at__date=today)
    
    # 今日の売上合計を計算（データがない場合は0円にする）
    total_sales = todays_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    # 今日の人気メニュー集計
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