from datetime import datetime, timezone
import re
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from starlette.requests import Request
from starlette.responses import JSONResponse

from .config import ALGORITHM, SECRET_KEY, TOKEN_EXPIRE_DELTA
from .data import get_route_role_cache, get_user_with_roles, user_has_permission, write_route_role_cache_file
from .models import Permission, Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

ROUTE_ROLE_CACHE: dict[str, dict[str, list[str]]] = {}
COMPILED_ROUTE_ROLE_RULES: list[tuple[str, str, re.Pattern[str], set[str]]] = []


def initialize_route_role_cache() -> None:
    global ROUTE_ROLE_CACHE, COMPILED_ROUTE_ROLE_RULES
    ROUTE_ROLE_CACHE = get_route_role_cache()
    write_route_role_cache_file(ROUTE_ROLE_CACHE)

    compiled_rules: list[tuple[str, str, re.Pattern[str], set[str]]] = []
    for path_template, method_map in ROUTE_ROLE_CACHE.items():
        for method, roles in method_map.items():
            regex_text = "^" + re.sub(r"\{[^/]+\}", r"[^/]+", path_template) + "$"
            compiled_rules.append((method, path_template, re.compile(regex_text), set(roles)))
    COMPILED_ROUTE_ROLE_RULES = compiled_rules


def _get_required_roles(method: str, path: str) -> set[str] | None:
    for rule_method, _, pattern, roles in COMPILED_ROUTE_ROLE_RULES:
        if rule_method == method and pattern.match(path):
            return roles
    return None


def _decode_and_load_user(token: str) -> dict:
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

    user = get_user_with_roles(username)
    if not user:
        raise cred_error

    return {"username": user["username"], "roles": user["roles"]}


async def rbac_middleware(request: Request, call_next):
    open_paths = {
        "/",
        "/auth/login",
        "/docs",
        "/redoc",
        "/openapi.json",
    }
    if request.url.path in open_paths:
        return await call_next(request)

    required_roles = _get_required_roles(request.method, request.url.path)
    if not required_roles:
        return await call_next(request)

    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Missing bearer token"},
        )

    token = auth_header.split(" ", 1)[1]
    try:
        user = _decode_and_load_user(token)
    except HTTPException as exc:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    if set(user["roles"]).isdisjoint(required_roles):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": f"Route requires one of roles: {sorted(required_roles)}"},
        )

    request.state.user = user
    return await call_next(request)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)


def authenticate_user(username: str, password: str) -> Optional[dict]:
    user = get_user_with_roles(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user


def create_access_token(username: str, roles: list[str]) -> str:
    payload = {
        "sub": username,
        "roles": roles,
        "exp": datetime.now(timezone.utc) + TOKEN_EXPIRE_DELTA,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    return _decode_and_load_user(token)


def require_role(*allowed_roles: Role):
    async def _guard(user: dict = Depends(get_current_user)):
        user_roles = set(user["roles"])
        if not any(role.value in user_roles for role in allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of: {[role.value for role in allowed_roles]}",
            )
        return user

    return _guard


def require_permission(permission: Permission):
    async def _guard(user: dict = Depends(get_current_user)):
        has_perm = user_has_permission(user["username"], permission.value)
        if not has_perm:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permission: {permission.value}",
            )
        return user

    return _guard
