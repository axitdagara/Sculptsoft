from datetime import date, timedelta
from decimal import Decimal

from fastapi import Body, Depends, FastAPI, Response, status
from sqlalchemy.orm import Session
import uvicorn

from api.error_handlers import register_exception_handlers
from config.db import get_db
from config.exceptions import DuplicateError, NotFoundError, ValidationError
from config.logger import get_logger
from models.orm_models import BookORM, BorrowHistoryORM, UserORM
from schemas import BookRead, BorrowActionResponse, BorrowHistoryRead, ErrorResponse, UserRead


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



@app.get(
    "/api/v1/books",
    response_model=list[BookRead],
    status_code=status.HTTP_200_OK,
    tags=["Books"],
    summary="List all books",
)
def list_books(db: Session = Depends(get_db)):
    return db.query(BookORM).order_by(BookORM.book_id.asc()).all()


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
    db: Session = Depends(get_db),
):
    title = title.strip()
    author = author.strip()

    if not title or not author:
        raise ValidationError("Title and author cannot be blank")

    duplicate = (
        db.query(BookORM)
        .filter(BookORM.title.ilike(title), BookORM.author.ilike(author))
        .first()
    )
    if duplicate is not None:
        raise DuplicateError("Book", f"{title} by {author}")

    book = BookORM(title=title, author=author, available=True)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@app.get(
    "/api/v1/books/{book_id}",
    response_model=BookRead,
    status_code=status.HTTP_200_OK,
    tags=["Books"],
    summary="Get a single book by ID",
    responses={404: {"model": ErrorResponse}},
)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookORM).filter(BookORM.book_id == book_id).first()
    if book is None:
        raise NotFoundError("Book", book_id)
    return book


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
    db: Session = Depends(get_db),
):
    book = db.query(BookORM).filter(BookORM.book_id == book_id).first()
    if book is None:
        raise NotFoundError("Book", book_id)

    data = {"title": title, "author": author, "available": available}
    data = {key: value for key, value in data.items() if value is not None}
    if not data:
        raise ValidationError("At least one field is required for update")

    if "title" in data:
        data["title"] = data["title"].strip()
        if not data["title"]:
            raise ValidationError("Title cannot be blank")

    if "author" in data:
        data["author"] = data["author"].strip()
        if not data["author"]:
            raise ValidationError("Author cannot be blank")

    for key, value in data.items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book


@app.delete(
    "/api/v1/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Books"],
    summary="Delete a book",
    responses={404: {"model": ErrorResponse}},
)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookORM).filter(BookORM.book_id == book_id).first()
    if book is None:
        raise NotFoundError("Book", book_id)

    db.delete(book)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get(
    "/api/v1/users",
    response_model=list[UserRead],
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    summary="List all users",
)
def list_users(db: Session = Depends(get_db)):
    return db.query(UserORM).order_by(UserORM.user_id.asc()).all()


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
    db: Session = Depends(get_db),
):
    name = name.strip()
    if not name:
        raise ValidationError("Name cannot be blank")

    duplicate = db.query(UserORM).filter(UserORM.name.ilike(name)).first()
    if duplicate is not None:
        raise DuplicateError("User", name)

    user = UserORM(
        name=name,
        borrow_limit=borrow_limit,
        borrow_days=borrow_days,
        fine_per_day=fine_per_day,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get(
    "/api/v1/users/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    summary="Get a single user by ID",
    responses={404: {"model": ErrorResponse}},
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserORM).filter(UserORM.user_id == user_id).first()
    if user is None:
        raise NotFoundError("User", user_id)
    return user


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
    db: Session = Depends(get_db),
):
    user = db.query(UserORM).filter(UserORM.user_id == user_id).first()
    if user is None:
        raise NotFoundError("User", user_id)

    data = {
        "name": name,
        "borrow_limit": borrow_limit,
        "borrow_days": borrow_days,
        "fine_per_day": fine_per_day,
    }
    data = {key: value for key, value in data.items() if value is not None}
    if not data:
        raise ValidationError("At least one field is required for update")

    if "name" in data:
        data["name"] = data["name"].strip()
        if not data["name"]:
            raise ValidationError("Name cannot be blank")

    for key, value in data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


@app.delete(
    "/api/v1/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Users"],
    summary="Delete a user",
    responses={404: {"model": ErrorResponse}},
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserORM).filter(UserORM.user_id == user_id).first()
    if user is None:
        raise NotFoundError("User", user_id)

    db.delete(user)
    db.commit()
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
    db: Session = Depends(get_db),
):
    user = db.query(UserORM).filter(UserORM.user_id == user_id).first()
    if user is None:
        raise NotFoundError("User", user_id)

    book = db.query(BookORM).filter(BookORM.book_id == book_id).first()
    if book is None:
        raise NotFoundError("Book", book_id)

    if not book.available:
        raise ValidationError(f"'{book.title}' is not available right now")

    active_count = (
        db.query(BorrowHistoryORM)
        .filter(
            BorrowHistoryORM.user_id == user_id,
            BorrowHistoryORM.returned_on.is_(None),
        )
        .count()
    )
    if active_count >= user.borrow_limit:
        raise ValidationError(f"Borrow limit reached ({user.borrow_limit} books)")

    borrowed_on = date.today()
    due_on = borrowed_on + timedelta(days=user.borrow_days)

    entry = BorrowHistoryORM(
        user_id=user_id,
        book_id=book_id,
        borrowed_on=borrowed_on,
        due_on=due_on,
        returned_on=None,
        fine=Decimal("0.00"),
    )
    book.available = False
    db.add(entry)
    db.commit()
    db.refresh(entry)

    return BorrowActionResponse(
        message=f"{user.name} borrowed {book.title}. Due on {due_on}.",
        user_id=user.user_id,
        book_id=book.book_id,
        book_title=book.title,
        borrowed_on=borrowed_on,
        due_on=due_on,
        fine=Decimal("0.00"),
    )


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
    db: Session = Depends(get_db),
):
    user = db.query(UserORM).filter(UserORM.user_id == user_id).first()
    if user is None:
        raise NotFoundError("User", user_id)

    book = db.query(BookORM).filter(BookORM.book_id == book_id).first()
    if book is None:
        raise NotFoundError("Book", book_id)

    borrow_row = (
        db.query(BorrowHistoryORM)
        .filter(
            BorrowHistoryORM.user_id == user_id,
            BorrowHistoryORM.book_id == book_id,
            BorrowHistoryORM.returned_on.is_(None),
        )
        .order_by(BorrowHistoryORM.borrowed_on.desc())
        .first()
    )
    if borrow_row is None:
        raise ValidationError(f"{user.name} has not borrowed {book.title}")

    returned_on = date.today()
    late_days = max((returned_on - borrow_row.due_on).days, 0)
    fine_per_day = user.fine_per_day if isinstance(user.fine_per_day, Decimal) else Decimal(str(user.fine_per_day))
    fine = Decimal(late_days) * fine_per_day

    borrow_row.returned_on = returned_on
    borrow_row.fine = fine
    book.available = True
    db.commit()

    if late_days > 0:
        message = f"{user.name} returned {book.title}. Late by {late_days} days. Fine: {fine:.2f}."
    else:
        message = f"{user.name} returned {book.title}. No fine."

    return BorrowActionResponse(
        message=message,
        user_id=user.user_id,
        book_id=book.book_id,
        book_title=book.title,
        due_on=borrow_row.due_on,
        returned_on=returned_on,
        fine=fine,
    )


@app.get(
    "/api/v1/users/{user_id}/borrow-history",
    response_model=list[BorrowHistoryRead],
    status_code=status.HTTP_200_OK,
    tags=["Borrowing"],
    summary="Get a user's borrow history",
    responses={404: {"model": ErrorResponse}},
)
def get_user_borrow_history(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserORM).filter(UserORM.user_id == user_id).first()
    if user is None:
        raise NotFoundError("User", user_id)

    rows = (
        db.query(BorrowHistoryORM, BookORM)
        .join(BookORM, BorrowHistoryORM.book_id == BookORM.book_id)
        .filter(BorrowHistoryORM.user_id == user_id)
        .order_by(BorrowHistoryORM.borrowed_on.desc(), BorrowHistoryORM.history_id.desc())
        .all()
    )

    return [
        BorrowHistoryRead(
            history_id=history.history_id,
            user_id=history.user_id,
            book_id=history.book_id,
            book_title=book.title,
            book_author=book.author,
            borrowed_on=history.borrowed_on,
            due_on=history.due_on,
            returned_on=history.returned_on,
            fine=history.fine,
        )
        for history, book in rows
    ]


if __name__ == "__main__":
    logger.info("Starting FastAPI app on http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)