# FastAPI Movie Recommender (MySQL)

## 1) Setup
```bash
cd backend_fastapi
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # then edit values
```

## 2) MySQL
Create DB + tables and seed sample data:
```bash
mysql -u root -p < sql/schema.sql
mysql -u root -p moviesdb < sql/seed.sql
```

## 3) Run
```bash
uvicorn app.main:app --reload --port 8000
```

## 4) API
- `GET /api/movies` — list movies (paged)
- `GET /api/users` — list users
- `GET /api/users/{user_id}/ratings` — a user's ratings
- `POST /api/users/{user_id}/ratings` — add/update a rating `{ "movie_id": 1, "rating": 4.5 }`
- `GET /api/recommend?user_id=1&limit=12` — personalized recommendations

Recommender is content-based (TF‑IDF over `genres`, `overview`) with aggregation over top‑rated movies by the user. Falls back to popularity when user is new.
