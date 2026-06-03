# RBAC FastAPI Demo

This is a small FastAPI app under `app/`.

## How It Works

SQLite stores users, roles, permissions, and route access. JWT checks the user login. RBAC middleware checks the user role. The route access list is saved in `route_roles_cache.json`.

The cache file uses this format:

```json
{
	"GET:/admin/users": ["admin", "manager"]
}
```

## Files

- `app/main.py` - app start
- `app/router.py` - API routes
- `app/controller.py` - route helpers
- `app/security.py` - login and role check
- `app/models.py` - data models
- `app/data.py` - database queries
- `app/db.py` - database setup and sample data
- `app/config.py` - settings
- `rbac.sqlite3` - database file
- `route_roles_cache.json` - route access file

## Install

```bash
pip install -r requirements.txt
```

Put your app settings in a root `.env` file.

## Run

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## Sample Users

- axit / secret123 (admin)
- harsh / secret123 (editor)
- tirth / secret123 (viewer)
- mansi / secret123 (manager)
