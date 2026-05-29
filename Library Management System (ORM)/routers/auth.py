from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.orm import Session

from config.db import get_db
from config.security import create_access_token
from models.orm_models import UserORM
from schemas import ErrorResponse, TokenResponse, UserLogin, UserRead
from services.auth import authenticate_user, get_current_user


public_router = APIRouter(prefix="/api/v1")
protected_router = APIRouter(prefix="/api/v1", dependencies=[Depends(get_current_user)])


@public_router.post(
    "/auth/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    tags=["Auth"],
    summary="Log in with name and password",
    responses={401: {"model": ErrorResponse}},
)
def login(credentials: UserLogin = Body(...), db: Session = Depends(get_db)):
    user = authenticate_user(db, credentials.name, credentials.password)
    token = create_access_token(subject=str(user.user_id), additional_claims={"name": user.name})
    return TokenResponse(access_token=token)


@protected_router.get(
    "/auth/me",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    tags=["Auth"],
    summary="Get the current authenticated user",
)
def get_me(current_user: UserORM = Depends(get_current_user)):
    return current_user