import qrcode
from django.shortcuts import render
from io import BytesIO
import base64

def generate_qr(request):
    # Renderで発行された新しいURLに書き換えました
    url = "https://laffle.onrender.com"
    
    # QRコードの作成
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # 画像をバイナリデータとして取得
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    
    # HTMLで表示できるようにBase64エンコード
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'store/qr_code.html', {'qr_code': qr_code_base64, 'url': url})