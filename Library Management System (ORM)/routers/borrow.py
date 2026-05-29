from fastapi import APIRouter, Body, Depends, status

from exceptions import UnauthorizedError
from models.orm_models import UserORM
from schemas import BorrowActionResponse, BorrowHistoryRead, ErrorResponse
from services.auth import get_current_user

from .dependencies import get_library


protected_router = APIRouter(prefix="/api/v1", dependencies=[Depends(get_current_user)])


@protected_router.post(
    "/borrow",
    response_model=BorrowActionResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Borrowing"],
    summary="Borrow a book",
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def borrow_book(
    user_id: int = Body(..., ge=1),
    book_id: int = Body(..., ge=1),
    current_user: UserORM = Depends(get_current_user),
    library=Depends(get_library),
):
    if user_id != current_user.user_id:
        raise UnauthorizedError("You can only borrow books for your own account")
    return library.borrow_book(current_user.user_id, book_id)


@protected_router.post(
    "/return",
    response_model=BorrowActionResponse,
    status_code=status.HTTP_200_OK,
    tags=["Borrowing"],
    summary="Return a book",
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def return_book(
    user_id: int = Body(..., ge=1),
    book_id: int = Body(..., ge=1),
    current_user: UserORM = Depends(get_current_user),
    library=Depends(get_library),
):
    if user_id != current_user.user_id:
        raise UnauthorizedError("You can only return books for your own account")
    return library.return_book(current_user.user_id, book_id)


@protected_router.get(
    "/users/{user_id}/borrow-history",
    response_model=list[BorrowHistoryRead],
    status_code=status.HTTP_200_OK,
    tags=["Borrowing"],
    summary="Get a user's borrow history",
    responses={404: {"model": ErrorResponse}},
)
def get_user_borrow_history(
    user_id: int,
    current_user: UserORM = Depends(get_current_user),
    library=Depends(get_library),
):
    if user_id != current_user.user_id:
        raise UnauthorizedError("You can only view your own borrow history")
    return library.get_user_borrow_history(user_id)