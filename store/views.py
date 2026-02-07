import qrcode
from django.shortcuts import render
from io import BytesIO
import base64
from .models import Product  # 商品データを読み込むために必要です

# 商品一覧を表示する機能（これが足りなかった！）
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

# QRコードを生成する機能
def generate_qr(request):
    url = "https://laffle.onrender.com"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'store/qr_code.html', {'qr_code': qr_code_base64, 'url': url})