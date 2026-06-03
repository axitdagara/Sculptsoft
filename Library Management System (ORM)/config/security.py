from __future__ import annotations

import os
import re
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from pathlib import Path

import dotenv
import jwt
from passlib.context import CryptContext
from fastapi import Request
from fastapi.responses import JSONResponse

from exceptions import ApplicationError, ForbiddenError, UnauthorizedError


dotenv.load_dotenv()

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
RBAC_PERMISSIONS_PATH = Path(__file__).resolve().parent.parent / "route_roles_cache.json"


def _get_jwt_secret() -> str:
    secret = os.getenv("JWT_SECRET") or os.getenv("jwt_secret") or "dev-secret-change-me-please-use-env"
    if not secret:
        raise UnauthorizedError("JWT secret is not configured")
    return secret


def _get_jwt_algorithm() -> str:
    return os.getenv("JWT_ALGORITHM") or "HS256"


def _get_jwt_expiry_minutes() -> int:
    raw_value = os.getenv("JWT_EXPIRES_MINUTES") or "60"
    try:
        return max(int(raw_value), 1)
    except ValueError as exc:
        raise UnauthorizedError("JWT expiry configuration is invalid") from exc


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str | None) -> bool:
    if not password_hash:
        return False

    try:
        return pwd_context.verify(password, password_hash)
    except Exception:
        return False


def create_access_token(subject: str, additional_claims: dict[str, str] | None = None) -> str:
    expiry = datetime.now(timezone.utc) + timedelta(minutes=_get_jwt_expiry_minutes())
    payload: dict[str, object] = {
        "sub": subject,
        "exp": expiry,
        "iat": datetime.now(timezone.utc),
    }
    if additional_claims:
        payload.update(additional_claims)
    return jwt.encode(payload, _get_jwt_secret(), algorithm=_get_jwt_algorithm())


def decode_access_token(token: str) -> dict[str, object]:
    try:
        return jwt.decode(token, _get_jwt_secret(), algorithms=[_get_jwt_algorithm()])
    except jwt.ExpiredSignatureError as exc:
        raise UnauthorizedError("Your token has expired") from exc
    except jwt.InvalidTokenError as exc:
        raise UnauthorizedError("Your token is invalid") from exc


@lru_cache(maxsize=1)
def load_route_roles() -> dict[str, dict[str, list[str]]]:
    import json

    if not RBAC_PERMISSIONS_PATH.exists():
        return {}

    with RBAC_PERMISSIONS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def _route_pattern_matches(route_pattern: str, request_path: str) -> bool:
    regex = "^" + re.sub(r"\{[^/]+\}", r"[^/]+", route_pattern.rstrip("/")) + "$"
    normalized_path = request_path.rstrip("/") or "/"
    return re.match(regex, normalized_path) is not None


def get_allowed_roles_for_request(method: str, path: str) -> list[str] | None:
    permissions = load_route_roles()
    normalized_method = method.upper()

    for route_pattern, methods in permissions.items():
        if _route_pattern_matches(route_pattern, path):
            return methods.get(normalized_method)

    return None


async def rbac_middleware(request: Request, call_next):
    try:
        if request.method.upper() == "OPTIONS":
            return await call_next(request)

        allowed_roles = get_allowed_roles_for_request(request.method, request.url.path)
        if allowed_roles is None:
            return await call_next(request)

        authorization = request.headers.get("Authorization", "")
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer" or not token:
            raise UnauthorizedError("Bearer token is required")

        payload = decode_access_token(token)
        role = str(payload.get("role", "")).lower()
        if role not in allowed_roles:
            raise ForbiddenError("Your role is not allowed to access this route")

        return await call_next(request)
    except ApplicationError as exc:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
