# Library Management API

FastAPI backend for managing a small library system with SQLAlchemy ORM, Alembic migrations, JWT authentication, and role-based access control.

## Features

- User registration and login with JWT access tokens
- Role support for `admin` and `user`
- RBAC route permissions loaded from `route_roles_cache.json`
- CRUD endpoints for books
- CRUD endpoints for users
- Borrow, return, and user borrow-history endpoints
- Centralized application exceptions and structured error handling
- PostgreSQL database access through SQLAlchemy ORM
- Alembic migrations for schema changes
- API docs enabled at `/docs`, `/redoc`, and `/openapi.json`

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy ORM
- Alembic
- PostgreSQL with `psycopg2`
- PyJWT
- Passlib
- python-dotenv

## Project Structure

```text
.
|-- alembic/
|   |-- versions/          # Database migrations
|   |-- env.py             # Alembic environment
|-- config/
|   |-- db.py              # Database session and engine setup
|   |-- logger.py          # Application logging
|   |-- security.py        # Password, JWT, and RBAC helpers
|-- models/
|   |-- orm_models.py      # SQLAlchemy models
|-- routers/
|   |-- auth.py            # Login and current-user routes
|   |-- books.py           # Book routes
|   |-- borrow.py          # Borrowing routes
|   |-- users.py           # User routes
|-- schemas/               # Pydantic request and response models
|-- services/
|   |-- auth.py            # Authentication service helpers
|   |-- library.py         # Library business service
|-- exceptions.py          # Custom application errors
|-- main.py                # FastAPI app entrypoint
|-- route_roles_cache.json # RBAC route permissions
|-- alembic.ini
|-- requirements.txt
`-- README.md
```

## Prerequisites

- Python 3.10 or later
- PostgreSQL database

## Quick Start

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create a local `.env` file:

```ini
host=localhost
user=postgres
password=YOUR_DB_PASSWORD
database=library_management
port=5432
JWT_SECRET=change-this-secret
JWT_ALGORITHM=HS256
JWT_EXPIRES_MINUTES=60
```

4. Apply migrations:

```powershell
alembic upgrade head
```

5. Run the development server:

```powershell
python main.py
```

Open the API documentation at:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`
- `http://127.0.0.1:8000/openapi.json`

## Endpoint Summary

Auth:

- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`

Users:

- `POST /api/v1/users`
- `GET /api/v1/users`
- `GET /api/v1/users/{user_id}`
- `PUT /api/v1/users/{user_id}`
- `DELETE /api/v1/users/{user_id}`

Books:

- `GET /api/v1/books`
- `POST /api/v1/books`
- `GET /api/v1/books/{book_id}`
- `PUT /api/v1/books/{book_id}`
- `DELETE /api/v1/books/{book_id}`

Borrowing:

- `POST /api/v1/borrow`
- `POST /api/v1/return`
- `GET /api/v1/users/{user_id}/borrow-history`

## Notes

- Keep `.env` out of version control.
- Use Alembic migrations for database schema changes.
- The current Alembic chain is `20260525_01 -> 20260526_01 -> 20260603_02`.
- `alembic/versions/20260603_01_add_user_role.py` is not part of the current migration chain.
