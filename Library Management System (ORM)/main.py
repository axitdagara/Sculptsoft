from decimal import Decimal

from fastapi import Body, Depends, FastAPI, Response, status
from sqlalchemy.orm import Session
import uvicorn

from api.error_handlers import register_exception_handlers
from config.db import get_db
from config.logger import get_logger
from schemas import BookRead, BorrowActionResponse, BorrowHistoryRead, ErrorResponse, UserRead
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

register_exception_handlers(app)


def get_library(db: Session = Depends(get_db)) -> Library:
    return Library(db)



@app.get(
    "/api/v1/books",
    response_model=list[BookRead],
    status_code=status.HTTP_200_OK,
    tags=["Books"],
    summary="List all books",
)
def list_books(library: Library = Depends(get_library)):
    return library.list_books()


@app.post(
    "/api/v1/books",
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


@app.get(
    "/api/v1/books/{book_id}",
    response_model=BookRead,
    status_code=status.HTTP_200_OK,
    tags=["Books"],
    summary="Get a single book by ID",
    responses={404: {"model": ErrorResponse}},
)
def get_book(book_id: int, library: Library = Depends(get_library)):
    return library.get_book(book_id)


@app.put(
    "/api/v1/books/{book_id}",
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


@app.delete(
    "/api/v1/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Books"],
    summary="Delete a book",
    responses={404: {"model": ErrorResponse}},
)
def delete_book(book_id: int, library: Library = Depends(get_library)):
    library.delete_book(book_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get(
    "/api/v1/users",
    response_model=list[UserRead],
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    summary="List all users",
)
def list_users(library: Library = Depends(get_library)):
    return library.list_users()


@app.post(
    "/api/v1/users",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
    summary="Create a new user",
    responses={400: {"model": ErrorResponse}, 409: {"model": ErrorResponse}},
)
def create_user(
    name: str = Body(..., min_length=1, max_length=255),
    borrow_limit: int = Body(default=3, ge=1, le=10),
    borrow_days: int = Body(default=14, ge=1, le=60),
    fine_per_day: Decimal = Body(default=Decimal("2.00"), ge=0),
    library: Library = Depends(get_library),
):
    return library.create_user(
        name=name,
        borrow_limit=borrow_limit,
        borrow_days=borrow_days,
        fine_per_day=fine_per_day,
    )


@app.get(
    "/api/v1/users/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    summary="Get a single user by ID",
    responses={404: {"model": ErrorResponse}},
)
def get_user(user_id: int, library: Library = Depends(get_library)):
    return library.get_user(user_id)


@app.put(
    "/api/v1/users/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    summary="Update a user",
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def update_user(
    user_id: int,
    name: str | None = Body(default=None, min_length=1, max_length=255),
    borrow_limit: int | None = Body(default=None, ge=1, le=10),
    borrow_days: int | None = Body(default=None, ge=1, le=60),
    fine_per_day: Decimal | None = Body(default=None, ge=0),
    library: Library = Depends(get_library),
):
    return library.update_user(
        user_id,
        name=name,
        borrow_limit=borrow_limit,
        borrow_days=borrow_days,
        fine_per_day=fine_per_day,
    )


@app.delete(
    "/api/v1/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Users"],
    summary="Delete a user",
    responses={404: {"model": ErrorResponse}},
)
def delete_user(user_id: int, library: Library = Depends(get_library)):
    library.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post(
    "/api/v1/borrow",
    response_model=BorrowActionResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Borrowing"],
    summary="Borrow a book",
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def borrow_book(
    user_id: int = Body(..., ge=1),
    book_id: int = Body(..., ge=1),
    library: Library = Depends(get_library),
):
    return library.borrow_book(user_id, book_id)


@app.post(
    "/api/v1/return",
    response_model=BorrowActionResponse,
    status_code=status.HTTP_200_OK,
    tags=["Borrowing"],
    summary="Return a book",
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def return_book(
    user_id: int = Body(..., ge=1),
    book_id: int = Body(..., ge=1),
    library: Library = Depends(get_library),
):
    return library.return_book(user_id, book_id)


@app.get(
    "/api/v1/users/{user_id}/borrow-history",
    response_model=list[BorrowHistoryRead],
    status_code=status.HTTP_200_OK,
    tags=["Borrowing"],
    summary="Get a user's borrow history",
    responses={404: {"model": ErrorResponse}},
)
def get_user_borrow_history(user_id: int, library: Library = Depends(get_library)):
    return library.get_user_borrow_history(user_id)


if __name__ == "__main__":
    logger.info("Starting FastAPI app on http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)