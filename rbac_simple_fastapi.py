from typing import Optional, List

from fastapi import Depends, FastAPI, HTTPException, Header, status
from pydantic import BaseModel

app = FastAPI(title="Simple FastAPI RBAC (no JWT)")

# --- Data (very simple, plaintext passwords for demo) -----------------
USERS_DB = {
    "alice": {"username": "alice", "email": "alice@example.com", "password": "secret123", "roles": ["admin"]},
    "bob":   {"username": "bob",   "email": "bob@example.com",   "password": "secret123", "roles": ["editor"]},
    "charlie": {"username": "charlie", "email": "charlie@example.com", "password": "secret123", "roles": ["viewer"]},
}

ROLE_PERMISSIONS = {
    "viewer": {"posts:read"},
    "editor": {"posts:read", "posts:write"},
    "admin":  {"posts:read", "posts:write", "posts:delete"},
}

POSTS_DB = [
    {"id": 1, "title": "Hello World", "body": "First post!", "author": "alice"},
    {"id": 2, "title": "FastAPI Tips", "body": "Use Depends().", "author": "bob"},
]


class LoginIn(BaseModel):
    username: str
    password: str


class PostIn(BaseModel):
    title: str
    body: str


def authenticate_user(username: str, password: str) -> Optional[dict]:
    user = USERS_DB.get(username)
    if not user or user["password"] != password:
        return None
    return {"username": user["username"], "roles": list(user["roles"])}


async def get_current_user(x_user: Optional[str] = Header(None)) -> dict:
    """
    Very simple auth: pass header `X-User: alice` with username.
    This is only for learning/demo — not for production.
    """
    if not x_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing X-User header")
    user = USERS_DB.get(x_user)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown user")
    return {"username": user["username"], "roles": list(user["roles"])}


def require_permission(permission: str):
    async def _guard(user: dict = Depends(get_current_user)):
        user_roles = user.get("roles", [])
        for r in user_roles:
            if permission in ROLE_PERMISSIONS.get(r, set()):
                return user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Missing permission: {permission}")
    return _guard


def require_role(*allowed_roles: str):
    async def _guard(user: dict = Depends(get_current_user)):
        user_roles = set(user.get("roles", []))
        if not any(r in user_roles for r in allowed_roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Requires one of: {allowed_roles}")
        return user
    return _guard


@app.post("/auth/login")
async def login(data: LoginIn):
    """Login with username/password. Returns simple text token (username).
    Use this token by setting header `X-User: <username>` on requests.
    """
    user = authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad credentials")
    return {"message": "login ok", "token": user["username"], "roles": user["roles"]}


@app.get("/auth/me")
async def me(user: dict = Depends(get_current_user)):
    return {"username": user["username"], "roles": user["roles"]}


@app.get("/posts")
async def list_posts(user: dict = Depends(require_permission("posts:read"))):
    return POSTS_DB


@app.get("/posts/{post_id}")
async def get_post(post_id: int, user: dict = Depends(require_permission("posts:read"))):
    post = next((p for p in POSTS_DB if p["id"] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.post("/posts", status_code=201)
async def create_post(payload: PostIn, user: dict = Depends(require_permission("posts:write"))):
    new_id = max((p["id"] for p in POSTS_DB), default=0) + 1
    new_post = {"id": new_id, "title": payload.title, "body": payload.body, "author": user["username"]}
    POSTS_DB.append(new_post)
    return new_post


@app.delete("/posts/{post_id}")
async def delete_post(post_id: int, user: dict = Depends(require_permission("posts:delete"))):
    global POSTS_DB
    post = next((p for p in POSTS_DB if p["id"] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    POSTS_DB = [p for p in POSTS_DB if p["id"] != post_id]
    return {"message": f"Post {post_id} deleted by {user['username']}"}


@app.get("/admin/users")
async def list_users(user: dict = Depends(require_role("admin"))):
    return [{"username": u["username"], "email": u["email"], "roles": u["roles"]} for u in USERS_DB.values()]
