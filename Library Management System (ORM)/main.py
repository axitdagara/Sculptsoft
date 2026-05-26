from fastapi import APIRouter, Body, Depends, FastAPI, Response, status
from sqlalchemy.orm import Session
import uvicorn

from config.db import get_db
from exceptions import UnauthorizedError
from config.security import create_access_token
from config.logger import get_logger
from models.orm_models import UserORM
from schemas import BookRead, BorrowActionResponse, BorrowHistoryRead, ErrorResponse, TokenResponse, UserCreate, UserLogin, UserRead, UserUpdate
from services.auth import authenticate_user, get_current_user
from services.library import Library


logger = get_logger(__name__)


app = FastAPI(
    title="Library Management API",
    description="CRUD API built with FastAPI, SQLAlchemy ORM and Alembic migrations.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


public_router = APIRouter(prefix="/api/v1")   ## baki 
protected_router = APIRouter(prefix="/api/v1", dependencies=[Depends(get_current_user)])


def get_library(db: Session = Depends(get_db)) -> Library:
    return Library(db)



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


@public_router.post(
    "/users",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
    summary="Register a new user",
    responses={400: {"model": ErrorResponse}, 409: {"model": ErrorResponse}},
)
def create_user(user: UserCreate = Body(...), library: Library = Depends(get_library)):
    return library.create_user(
        name=user.name,
        password=user.password,
        borrow_limit=user.borrow_limit,
        borrow_days=user.borrow_days,
        fine_per_day=user.fine_per_day,
    )



@protected_router.get(
    "/books",
    response_model=list[BookRead],
    status_code=status.HTTP_200_OK,
    tags=["Books"],
    summary="List all books",
)
def list_books(library: Library = Depends(get_library)):
    return library.list_books()


@protected_router.post(
    "/books",
    response_model=BookRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Books"],
    summary="Create a new book",
    responses={400: {"model": ErrorResponse}, 409: {"model": ErrorResponse}},
)
def create_book(
    title: str = Body(..., min_length=1, max_length=255),
    author: str = Body(..., min_length=1, max_length=255),
    library: Library = Depends(get_library),
):
    return library.create_book(title, author)


@protected_router.get(
    "/books/{book_id}",
    response_model=BookRead,
    status_code=status.HTTP_200_OK,
    tags=["Books"],
    summary="Get a single book by ID",
    responses={404: {"model": ErrorResponse}},
)
def get_book(book_id: int, library: Library = Depends(get_library)):
    return library.get_book(book_id)


@protected_router.put(
    "/books/{book_id}",
    response_model=BookRead,
    status_code=status.HTTP_200_OK,
    tags=["Books"],
    summary="Update a book",
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def update_book(
    book_id: int,
    title: str | None = Body(default=None, min_length=1, max_length=255),
    author: str | None = Body(default=None, min_length=1, max_length=255),
    available: bool | None = Body(default=None),
    library: Library = Depends(get_library),
):
    return library.update_book(book_id, title=title, author=author, available=available)


@protected_router.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Books"],
    summary="Delete a book",
    responses={404: {"model": ErrorResponse}},
)
def delete_book(book_id: int, library: Library = Depends(get_library)):
    library.delete_book(book_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@protected_router.get(
    "/users",
    response_model=list[UserRead],
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    summary="List all users",
)
def list_users(library: Library = Depends(get_library)):
    return library.list_users()


@protected_router.get(
    "/users/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    summary="Get a single user by ID",
    responses={404: {"model": ErrorResponse}},
)
def get_user(user_id: int, library: Library = Depends(get_library)):
    return library.get_user(user_id)


@protected_router.put(
    "/users/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    summary="Update a user",
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def update_user(user_id: int, user: UserUpdate = Body(...), library: Library = Depends(get_library)):
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
def delete_user(user_id: int, library: Library = Depends(get_library)):
    library.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


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
    library: Library = Depends(get_library),
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
    library: Library = Depends(get_library),
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
    library: Library = Depends(get_library),
):
    if user_id != current_user.user_id:
        raise UnauthorizedError("You can only view your own borrow history")
    return library.get_user_borrow_history(user_id)


app.include_router(public_router)
app.include_router(protected_router)


if __name__ == "__main__":
    logger.info("Starting FastAPI app on http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)