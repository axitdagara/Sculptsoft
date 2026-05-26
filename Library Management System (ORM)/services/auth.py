from __future__ import annotations

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from config.db import get_db
from exceptions import UnauthorizedError
from config.security import decode_access_token, verify_password
from models.orm_models import UserORM


bearer_scheme = HTTPBearer(auto_error=False)


def authenticate_user(session: Session, name: str, password: str) -> UserORM:
    user = session.query(UserORM).filter(UserORM.name.ilike(name.strip())).first()
    if user is None or not verify_password(password, user.password_hash):
        raise UnauthorizedError("Invalid name or password")
    return user


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    session: Session = Depends(get_db),
) -> UserORM:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise UnauthorizedError("Bearer token is required")

    payload = decode_access_token(credentials.credentials)
    subject = payload.get("sub")
    if subject is None:
        raise UnauthorizedError("Token payload is missing the user id")

    try:
        user_id = int(subject)
    except (TypeError, ValueError) as exc:
        raise UnauthorizedError("Token payload is invalid") from exc

    user = session.query(UserORM).filter(UserORM.user_id == user_id).first()
    if user is None:
        raise UnauthorizedError("User no longer exists")
    return user