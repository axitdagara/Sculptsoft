from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import dotenv
import jwt
from passlib.context import CryptContext

from exceptions import UnauthorizedError


dotenv.load_dotenv()

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


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