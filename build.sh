#!/usr/bin/env bash
# エラーが出たらそこでストップする設定
set -o errexit

# 1. 必要なソフトをインストール
pip install -r requirements.txt

# 2. データベースを更新（ここが重要！）
python manage.py migrate

# 3. 画像などの準備
python manage.py collectstatic --no-input