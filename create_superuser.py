import os
import django

# Djangoの設定を読み込む
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = "admin"
password = "laffle1234"
email = "admin@example.com"

# ユーザーがいなければ作る、いれば何もしない
if not User.objects.filter(username=username).exists():
    print(f"Creating superuser: {username}")
    User.objects.create_superuser(username, email, password)
else:
    print(f"Superuser {username} already exists.")