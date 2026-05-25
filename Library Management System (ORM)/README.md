# Library Management API

This project is a clean, internship-level backend built with FastAPI, SQLAlchemy ORM, and Alembic. It provides documented CRUD APIs for library users and books with proper HTTP status codes and structured error responses.

## Features

## Tech Stack

## Project Structure
```text
.
|-- alembic/
|   |-- versions/
# Library Management API

This repository contains a simple internship-level backend API for managing a small library. It is built with FastAPI, SQLAlchemy ORM, and Alembic for migrations. The application is API-first. OpenAPI docs have been disabled in this project.

## Highlights
- CRUD endpoints for `books` and `users` under the `/api/v1` prefix
- SQLAlchemy models in `models/` and Pydantic schemas in `schemas/`
- Centralized error handling with consistent JSON responses
- Alembic migration scripts in `alembic/` for schema changes

## Prerequisites
- Python 3.10 or later
- PostgreSQL database accessible from your machine

## Quick start

1. Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install the required packages:

```powershell
pip install -r requirements.txt
```

3. Create a local `.env` file (DO NOT commit this file). Example:

```ini
# .env (example - keep secrets out of version control)
host=localhost
user=postgres
password=YOUR_DB_PASSWORD
database=library_managementt
port=5432
```

4. Apply database migrations:

```powershell
alembic upgrade head
```

5. Run the application (development):

```powershell
python main.py
```

Note: API documentation endpoints (Swagger/ReDoc/OpenAPI JSON) are disabled in this project.

## API endpoints (summary)

Books (`/api/v1/books`):
- `GET /` — list books (200)
- `POST /` — create book (201)
- `GET /{book_id}` — get book (200 or 404)
- `PUT /{book_id}` — update book (200)
- `DELETE /{book_id}` — delete book (204)

Users (`/api/v1/users`):
- `GET /` — list users (200)
- `POST /` — create user (201)
- `GET /{user_id}` — get user (200 or 404)
- `PUT /{user_id}` — update user (200)
- `DELETE /{user_id}` — delete user (204)

## Error responses
All handled errors return JSON of the form:

```json
{
    "error": "ErrorType",
    "message": "Human readable message"
}
```

## Project layout

```
.
|-- alembic/                # alembic migration scripts
|-- api/                    # FastAPI routers and error handlers
|-- config/                 # DB wiring and application exceptions
|-- models/                 # SQLAlchemy ORM mappings
|-- schemas/                # Pydantic request/response schemas
|-- main.py                 # FastAPI entrypoint
|-- alembic.ini
|-- requirements.txt
`-- README.md
```

## Best practices & notes
- Keep `.env` out of version control; add it to `.gitignore`.
- Use Alembic to modify schema rather than editing DB files directly.
- For production, add authentication, logging configuration, and containerization (Docker).

## Want examples?
I can add a Postman collection or example `curl` snippets for each endpoint — let me know which you'd prefer.
