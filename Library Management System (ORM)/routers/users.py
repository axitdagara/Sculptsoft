from fastapi import APIRouter, Body, Depends, Response, status

from schemas import ErrorResponse, UserCreate, UserRead, UserUpdate
from services.auth import get_current_user

from .dependencies import get_library


public_router = APIRouter(prefix="/api/v1")
protected_router = APIRouter(prefix="/api/v1", dependencies=[Depends(get_current_user)])


@public_router.post(
    "/users",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
    summary="Register a new user",
    responses={400: {"model": ErrorResponse}, 409: {"model": ErrorResponse}},
)
def create_user(user: UserCreate = Body(...), library=Depends(get_library)):
    return library.create_user(
        name=user.name,
        password=user.password,
        borrow_limit=user.borrow_limit,
        borrow_days=user.borrow_days,
        fine_per_day=user.fine_per_day,
    )


@protected_router.get(
    "/users",
    response_model=list[UserRead],
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    summary="List all users",
)
def list_users(library=Depends(get_library)):
    return library.list_users()


@protected_router.get(
    "/users/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    summary="Get a single user by ID",
    responses={404: {"model": ErrorResponse}},
)
def get_user(user_id: int, library=Depends(get_library)):
    return library.get_user(user_id)


@protected_router.put(
    "/users/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    summary="Update a user",
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def update_user(user_id: int, user: UserUpdate = Body(...), library=Depends(get_library)):
    return library.update_user(
        user_id,
        name=user.name,
        password=user.password,
        borrow_limit=user.borrow_limit,
        borrow_days=user.borrow_days,
        fine_per_day=user.fine_per_day,
    )


@protected_router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Users"],
    summary="Delete a user",
    responses={404: {"model": ErrorResponse}},
)
def delete_user(user_id: int, library=Depends(get_library)):
    library.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)