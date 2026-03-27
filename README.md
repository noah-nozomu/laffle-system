# 🧇 Laffle Order System

飲食店向けのモバイルオーダーWebアプリです。  
実際のワッフル店舗で運用し、QRコードによるセルフ注文を実現しました。

---

## 🔗 リンク

| | URL |
|---|---|
| デモ | https://laffle.onrender.com/demo/ |
| 本番 | https://laffle.onrender.com |

> ※ デモURLでは実際の注文は送信されません。自由にお試しください。

---

## 📱 主な機能

- **QRコードで注文**：テーブルのQRを読み込むだけでメニューにアクセス
- **カテゴリ別メニュー表示**：ワッフル・ドリンクをカテゴリで切り替え
- **カート機能**：数量変更・削除・温度選択に対応
- **キッチンダッシュボード**：リアルタイムで未完了注文を一覧表示
- **売上集計**：当日の売上合計・商品別販売数を自動集計
- **注文編集・削除**：提供後の数量変更やキャンセルに対応

---

## 🛠 使用技術

| 分類 | 技術 |
|---|---|
| バックエンド | Python / Django |
| データベース | PostgreSQL (Neon) |
| 画像ストレージ | Cloudinary |
| ホスティング | Render |

---

## 💡 工夫した点

- **デバイスIDをCookieで管理**し、同一デバイスからの重複注文を防止
- **セッションでカートを管理**することでログイン不要なUXを実現
- キッチン側とお客様側で画面を分離し、**役割に応じたUIを設計**
- ポートフォリオ公開時の冷やかし注文対策として、`/demo/` URLではDBに保存しないデモモードを実装

---

## 📸 スクリーンショット
![オーダートップ画面](https://github.com/user-attachments/assets/a5fdbd6e-d188-4819-a572-10656f7ad862)
[商品選択画面](https://github.com/user-attachments/assets/b0519a3d-fab8-42d7-be7f-f0de63c9d9c6)
 ![注文確認画面](https://github.com/user-attachments/assets/627693c0-b9b1-429f-a9cb-b9d2affc2a80)
<img width="1916" height="967" alt="キッチン側画面" src="https://github.com/user-attachments/assets/8d9dfdec-fa46-4ec3-b1cf-f444fe5aad14" />
<!-- スクリーンシ!
ョットをここに追加

-->

---

## ⚙️ ローカル起動方法

```bash
git clone https://github.com/noah-nozomu/laffle-system
cd laffle-system
pip install -r requirements.txt

# .envファイルを作成してDATABASE_URLなどを設定
python manage.py migrate
python manage.py runserver
```
