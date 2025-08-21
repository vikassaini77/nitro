# File Parser CRUD API — Pro PG Edition
FastAPI + PostgreSQL + Celery + Redis + JWT + Docker Compose

## Run
```bash
cp .env.example .env
docker compose up --build
```
Open http://localhost:8000/docs

### Use
1) POST /auth/token (username `admin`, password `admin123`)
2) Authorize (Bearer token) in Swagger
3) POST /files → upload CSV/XLSX/TXT
4) GET /files/{id}/progress or WebSocket `ws://localhost:8000/ws/files/{id}/progress`
5) GET /files/{id} for parsed JSON
6) GET /files and DELETE /files/{id}