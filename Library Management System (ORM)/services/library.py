from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from exceptions import DuplicateError, NotFoundError, ValidationError
from config.logger import get_logger
from config.security import hash_password
from models.orm_models import BookORM, BorrowHistoryORM, UserORM
from schemas import BorrowActionResponse, BorrowHistoryRead


logger = get_logger(__name__)


class Library:
    def __init__(self, session: Session):
        self.session = session

    def list_books(self):
        return self.session.query(BookORM).order_by(BookORM.book_id.asc()).all()

    def create_book(self, title: str, author: str):
        title = title.strip()
        author = author.strip()

        if not title or not author:
            raise ValidationError("Title and author cannot be blank")

        duplicate = (
            self.session.query(BookORM)
            .filter(BookORM.title.ilike(title), BookORM.author.ilike(author))
            .first()
        )
        if duplicate is not None:
            raise DuplicateError("Book", f"{title} by {author}")

        try:
            book = BookORM(title=title, author=author, available=True)
            self.session.add(book)
            self.session.commit()
            self.session.refresh(book)
            return book
        except IntegrityError:
            self.session.rollback()
            raise DuplicateError("Book", f"{title} by {author}")
        except SQLAlchemyError:
            self.session.rollback()
            logger.exception("Database error while creating book title=%s", title)
            raise

    def get_book(self, book_id: int):
        book = self.session.query(BookORM).filter(BookORM.book_id == book_id).first()
        if book is None:
            raise NotFoundError("Book", book_id)
        return book

    def update_book(
        self,
        book_id: int,
        title: str | None = None,
        author: str | None = None,
        available: bool | None = None,
    ):
        book = self.get_book(book_id)

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

        self.session.commit()
        self.session.refresh(book)
        return book

    def delete_book(self, book_id: int):
        book = self.get_book(book_id)
        self.session.delete(book)
        self.session.commit()

    def list_users(self):
        return self.session.query(UserORM).order_by(UserORM.user_id.asc()).all()

    def create_user(
        self,
        name: str,
        password: str,
        borrow_limit: int = 3,
        borrow_days: int = 14,
        fine_per_day: Decimal = Decimal("2.00"),
    ):
        name = name.strip()
        if not name:
            raise ValidationError("Name cannot be blank")

        duplicate = self.session.query(UserORM).filter(UserORM.name.ilike(name)).first()
        if duplicate is not None:
            raise DuplicateError("User", name)

        try:
            user = UserORM(
                name=name,
                password_hash=hash_password(password),
                borrow_limit=borrow_limit,
                borrow_days=borrow_days,
                fine_per_day=fine_per_day,
            )
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except IntegrityError:
            self.session.rollback()
            raise DuplicateError("User", name)
        except SQLAlchemyError:
            self.session.rollback()
            logger.exception("Database error while creating user name=%s", name)
            raise

    def get_user(self, user_id: int):
        user = self.session.query(UserORM).filter(UserORM.user_id == user_id).first()
        if user is None:
            raise NotFoundError("User", user_id)
        return user

    def update_user(
        self,
        user_id: int,
        name: str | None = None,
        password: str | None = None,
        borrow_limit: int | None = None,
        borrow_days: int | None = None,
        fine_per_day: Decimal | None = None,
    ):
        user = self.get_user(user_id)

        data = {
            "name": name,
            "password": password,
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

            duplicate = (
                self.session.query(UserORM)
                .filter(UserORM.user_id != user_id, UserORM.name.ilike(data["name"]))
                .first()
            )
            if duplicate is not None:
                raise DuplicateError("User", data["name"])

        if "password" in data:
            data["password_hash"] = hash_password(data.pop("password"))

        for key, value in data.items():
            if key == "password_hash":
                user.password_hash = value
            else:
                setattr(user, key, value)

        self.session.commit()
        self.session.refresh(user)
        return user

    def delete_user(self, user_id: int):
        user = self.get_user(user_id)
        self.session.delete(user)
        self.session.commit()

    def borrow_book(self, user_id: int, book_id: int):
        user = self.get_user(user_id)
        book = self.get_book(book_id)

        if not book.available:
            raise ValidationError(f"'{book.title}' is not available right now")

        active_count = (
            self.session.query(func.count())
            .select_from(BorrowHistoryORM)
            .filter(
                BorrowHistoryORM.user_id == user_id,
                BorrowHistoryORM.returned_on.is_(None),
            )
            .scalar()
        )
        if active_count >= user.borrow_limit:
            raise ValidationError(f"Borrow limit reached ({user.borrow_limit} books)")

        borrowed_on = date.today()
        due_on = borrowed_on + timedelta(days=user.borrow_days)

        try:
            entry = BorrowHistoryORM(
                user_id=user_id,
                book_id=book_id,
                borrowed_on=borrowed_on,
                due_on=due_on,
                returned_on=None,
                fine=Decimal("0.00"),
            )
            book.available = False
            self.session.add(entry)
            self.session.commit()
            self.session.refresh(entry)
            return BorrowActionResponse(
                message=f"{user.name} borrowed {book.title}. Due on {due_on}.",
                user_id=user.user_id,
                book_id=book.book_id,
                book_title=book.title,
                borrowed_on=borrowed_on,
                due_on=due_on,
                fine=Decimal("0.00"),
            )
        except SQLAlchemyError:
            self.session.rollback()
            logger.exception("Database error while borrowing book_id=%s user_id=%s", book_id, user_id)
            raise

    def return_book(self, user_id: int, book_id: int):
        user = self.get_user(user_id)
        book = self.get_book(book_id)

        borrow_row = (
            self.session.query(BorrowHistoryORM)
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
        fine_per_day = user.fine_per_day if isinstance(user.fine_per_day, Decimal) else Decimal(str(user.fine_per_day))
        late_days = max((returned_on - borrow_row.due_on).days, 0)
        fine = Decimal(late_days) * fine_per_day

        try:
            borrow_row.returned_on = returned_on
            borrow_row.fine = fine
            book.available = True
            self.session.commit()

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
        except SQLAlchemyError:
            self.session.rollback()
            logger.exception("Database error while returning book_id=%s user_id=%s", book_id, user_id)
            raise

    def get_user_borrow_history(self, user_id: int):
        self.get_user(user_id)

        rows = (
            self.session.query(BorrowHistoryORM, BookORM)
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
