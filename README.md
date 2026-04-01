# Travel Planner AI 🗺️

ユーザーが行きたいスポットを入力すると、距離や効率を考慮した旅行プラン（観光地・宿泊・移動順）をタイムスケジュール形式で提案するWebアプリです。

## 技術スタック

| レイヤー | 技術 |
|---------|------|
| フロントエンド | React 19 + TypeScript (Vite) |
| バックエンド | FastAPI (Python 3.12) |
| DB | SQLite |
| インフラ | Docker Compose |

## 主な機能

- スポットの登録（名前・住所・座標）
- OpenStreetMap Nominatim APIによる座標自動取得
- Haversine公式 + 最近傍法によるルート最適化
- エリアベースの宿泊地提案
- 日ごとのタイムスケジュール表示

## セットアップ

### Docker（推奨）

```bash
docker compose up --build
```

- フロントエンド: http://localhost:5173
- バックエンドAPI: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

### ローカル開発

**バックエンド:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**フロントエンド:**
```bash
cd frontend
npm install
npm run dev
```

## API エンドポイント

| Method | Endpoint | 説明 |
|--------|----------|------|
| GET | `/api/health` | ヘルスチェック |
| POST | `/api/spots` | スポット登録 |
| GET | `/api/spots` | スポット一覧取得 |
| DELETE | `/api/spots/{id}` | スポット削除 |
| POST | `/api/trips` | 旅行プラン生成 |
| GET | `/api/trips/{id}` | プラン詳細取得 |

## ディレクトリ構成

```
travel-planner-ai/
├── docker-compose.yml
├── frontend/          # React + TypeScript (Vite)
│   ├── src/
│   │   ├── api/       # APIクライアント
│   │   ├── components/ # UIコンポーネント
│   │   ├── pages/     # ページコンポーネント
│   │   └── types/     # TypeScript型定義
│   └── Dockerfile
├── backend/           # FastAPI
│   ├── app/
│   │   ├── models/    # SQLAlchemyモデル
│   │   ├── schemas/   # Pydanticスキーマ
│   │   ├── routers/   # APIルーター
│   │   └── services/  # ビジネスロジック
│   ├── tests/
│   └── Dockerfile
└── README.md
```

## テスト

```bash
cd backend
pip install -r requirements.txt
pytest
```