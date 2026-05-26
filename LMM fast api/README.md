# Library Management System (FastAPI)

Simple Library Management System using FastAPI, SQLAlchemy and PostgreSQL.

Features
- Add / remove books
- Register users
- Lend and return books
- Search books by title/author
- Borrow limit, simple fine calculation
- Logging

Prerequisites
- Python 3.11+
- PostgreSQL server (create a database named `llm`)

Configuration
Edit `.env` if needed (defaults provided):

- `DATABASE_USER` (default `postgres`)
- `DATABASE_PASSWORD` (default `123456789`)
- `DATABASE_HOST` (default `localhost`)
- `DATABASE_NAME` (default `llm`)

Install

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # PowerShell
pip install -r requirements.txt
```

Database migrations (Alembic)

Initialize DB (ensure Postgres is running and `llm` DB exists):

```bash
alembic upgrade head
```

Run

```bash
uvicorn app.main:app --reload
```

API

Open docs at `http://127.0.0.1:8000/docs`

Sample output

- POST /books/ -> creates a book
- POST /users/ -> creates a user
- POST /lend/{book_id}/to/{user_id} -> lends a book
- POST /return/{book_id}/from/{user_id} -> returns and computes fine
