

from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


SECRET_KEY = "super-secret-key-change-in-prod"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

class Role(str, Enum):
    ADMIN  = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"

class Permission(str, Enum):
    READ   = "posts:read"
    WRITE  = "posts:write"
    DELETE = "posts:delete"

ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    Role.VIEWER: {Permission.READ},
    Role.EDITOR: {Permission.READ, Permission.WRITE},
    Role.ADMIN:  {Permission.READ, Permission.WRITE, Permission.DELETE},
}

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")   ###BAKI 

USERS_DB: dict[str, dict] = {
    "axit": {
        "username": "axit",
        "email": "axit@example.com",
        "hashed_password": pwd_ctx.hash("secret123"),
        "roles": [Role.ADMIN],
    },
    "harsh": {
        "username": "harsh",
        "email": "harsh@example.com",
        "hashed_password": pwd_ctx.hash("secret123"),
        "roles": [Role.EDITOR],
    },
    "tirth": {
        "username": "tirth",
        "email": "tirth@example.com",
        "hashed_password": pwd_ctx.hash("secret123"),
        "roles": [Role.VIEWER],
    },
}

POSTS_DB: list[dict] = [
    {"id": 1, "title": "Hello World", "body": "First post!", "author": "axit"},
    {"id": 2, "title": "FastAPI Tips", "body": "Use Depends().", "author": "harsh"},
]

class Token(BaseModel):
    access_token: str
    token_type: str
    roles: list[str]

class UserOut(BaseModel):
    username: str
    email: str
    roles: list[str]

class PostCreate(BaseModel):
    title: str
    body: str

class PostOut(BaseModel):
    id: int
    title: str
    body: str
    author: str



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)

def authenticate_user(username: str, password: str) -> Optional[dict]:
    user = USERS_DB.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user

def create_access_token(username: str, roles: list[str]) -> str:
    payload = {
        "sub":   username,
        "roles": roles,
        "exp":   datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    cred_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise cred_error
    except JWTError:
        raise cred_error

    user = USERS_DB.get(username)
    if not user:
        raise cred_error
    return {"username": username, "roles": [r.value for r in user["roles"]]}


def require_role(*allowed_roles: Role):

    async def _guard(user: dict = Depends(get_current_user)):
        user_roles = set(user["roles"])
        if not any(r.value in user_roles for r in allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of: {[r.value for r in allowed_roles]}",
            )
        return user
    return _guard

def require_permission(permission: Permission):
   
    async def _guard(user: dict = Depends(get_current_user)):
        user_roles = {Role(r) for r in user["roles"] if r in Role._value2member_map_}
        has_perm = any(permission in ROLE_PERMISSIONS.get(r, set()) for r in user_roles)
        if not has_perm:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permission: {permission.value}",
            )
        return user
    return _guard


app = FastAPI(
    title="FastAPI RBAC Demo",
    description= "RBAS",

    version="1.0.0",
)


@app.post("/auth/login", response_model=Token, tags=["Auth"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login with username + password → get a JWT token."""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    roles = [r.value for r in user["roles"]]
    token = create_access_token(user["username"], roles)
    return Token(access_token=token, token_type="bearer", roles=roles)

@app.get("/auth/me", response_model=UserOut, tags=["Auth"])
async def me(user: dict = Depends(get_current_user)):
    """Returns the currently authenticated user's info."""
    db_user = USERS_DB[user["username"]]
    return UserOut(
        username=db_user["username"],
        email=db_user["email"],
        roles=[r.value for r in db_user["roles"]],
    )


@app.get("/posts", response_model=list[PostOut], tags=["Posts"])
async def list_posts(_: dict = Depends(require_permission(Permission.READ))):
    return POSTS_DB

@app.get("/posts/{post_id}", response_model=PostOut, tags=["Posts"])
async def get_post(
    post_id: int,
    user: dict = Depends(require_permission(Permission.READ)),
):
   
    post = next((p for p in POSTS_DB if p["id"] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.post("/posts", response_model=PostOut, status_code=201, tags=["Posts"])
async def create_post(
    post: PostCreate,
    user: dict = Depends(require_permission(Permission.WRITE)),
):
   
    new_post = {
        "id":     len(POSTS_DB) + 1,
        "title":  post.title,
        "body":   post.body,
        "author": user["username"],
    }
    POSTS_DB.append(new_post)
    return new_post

@app.delete("/posts/{post_id}", tags=["Posts"])
async def delete_post(
    post_id: int,
    user: dict = Depends(require_permission(Permission.DELETE)),
):
    global POSTS_DB
    post = next((p for p in POSTS_DB if p["id"] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    POSTS_DB = [p for p in POSTS_DB if p["id"] != post_id]
    return {"message": f"Post {post_id} deleted by {user['username']}"}


@app.get("/admin/users", tags=["Admin"])
async def list_users(user: dict = Depends(require_role(Role.ADMIN))):
  
    return [
        {"username": u["username"], "email": u["email"], "roles": [r.value for r in u["roles"]]}
        for u in USERS_DB.values()
    ]

@app.get("/admin/permissions", tags=["Admin"])
async def list_permissions(user: dict = Depends(require_role(Role.ADMIN))):
    
    return {
        role.value: [p.value for p in perms]
        for role, perms in ROLE_PERMISSIONS.items()
    }

@app.get("/", tags=["Info"])
async def root():
    return {
        "message": "FastAPI RBAC Demo",
        "docs": "/docs",
        "users": {
            "axit":   {"role": "admin",  "password": "secret123"},
            "harsh":  {"role": "editor", "password": "secret123"},
            "tirth":  {"role": "viewer", "password": "secret123"},
        },
    }