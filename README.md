# KNGW TEA PRODUCTION

茶生産管理システム - お茶の生産、出荷、在庫を一元管理するWebアプリケーション

## 機能

- 生産管理
  - 茶種別の生産記録
  - 品質チェック情報の記録
  - 生産日・数量の管理

- 出荷管理
  - 顧客別の出荷記録
  - 出荷日・数量の追跡
  - 出荷履歴の管理

- 在庫管理
  - リアルタイムの在庫状況
  - 茶種別の在庫追跡
  - 在庫履歴の確認

## 技術スタック

- Python 3.9
- Django 4.2.20
- Bootstrap 5.3
- SQLite3

## セットアップ

1. リポジトリのクローン:
```bash
git clone https://github.com/io0323/tea-production.git
cd tea-production
```

2. 仮想環境の作成と有効化:
```bash
python -m venv venv
source venv/bin/activate  # Unix/macOS
# または
.\venv\Scripts\activate  # Windows
```

3. 依存関係のインストール:
```bash
pip install -r requirements.txt
```

4. データベースのマイグレーション:
```bash
python manage.py migrate
```

5. 管理者ユーザーの作成:
```bash
python manage.py createsuperuser
```

6. 開発サーバーの起動:
```bash
python manage.py runserver
```

## 使用方法

1. ブラウザで http://127.0.0.1:8000 にアクセス
2. 管理画面（ http://127.0.0.1:8000/admin ）で各種データを管理
3. 生産・出荷・在庫の登録と確認

## ライセンス

MIT License

## 作者

io0323 