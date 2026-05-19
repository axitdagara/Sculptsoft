from config.db import get_session, get_engine, Base
from models.book import Book
from models.user import User
from models.orm_models import BookORM, UserORM, BorrowHistoryORM
from datetime import date, timedelta
from sqlalchemy import select, func, and_, update, or_
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from config.exceptions import NotFoundError, ValidationError, DuplicateError
from config.logger import get_logger


logger = get_logger(__name__)


class Library:
    def __init__(self):
        self.session = get_session()
        self._ensure_tables()

    def _ensure_tables(self):
        try:
            logger.info("Ensuring database tables exist")
            engine = get_engine()
            Base.metadata.create_all(bind=engine)
        except SQLAlchemyError:
            logger.exception("Failed while creating tables")
            raise

    def create_book(self, title, author):
      
        if not title or not title.strip():
            raise ValueError("Book title cannot be empty")
        if not author or not author.strip():
            raise ValueError("Book author cannot be empty")

        try:
            logger.info("Creating book title=%s", title)
            new_book = BookORM(title=title, author=author, available=True)
            self.session.add(new_book)
            self.session.commit()
            self.session.refresh(new_book)
            return Book(new_book.book_id, title, author, True)
        except IntegrityError:
            self.session.rollback()
            logger.warning("Duplicate book detected title=%s", title)
            raise DuplicateError("Book", title)
        except SQLAlchemyError:
            self.session.rollback()
            logger.exception("Database error while creating book title=%s", title)
            raise

    def create_user(self, name):
        
        if not name or not name.strip():
            raise ValueError("User name cannot be empty")

        try:
            logger.info("Creating user name=%s", name)
            new_user = UserORM(name=name, borrow_limit=3, borrow_days=14, fine_per_day=2.0)
            self.session.add(new_user)
            self.session.commit()
            self.session.refresh(new_user)
            return User(new_user.user_id, name)
        except IntegrityError:
            self.session.rollback()
            logger.warning("Duplicate user detected name=%s", name)
            raise DuplicateError("User", name)
        except SQLAlchemyError:
            self.session.rollback()
            logger.exception("Database error while creating user name=%s", name)
            raise

    def add_book(self, book):
        
        if not book or not book.title or not book.author:
            raise ValueError("Book object must have title and author")

        try:
            book_orm = BookORM(title=book.title, author=book.author, available=book.available)
            self.session.add(book_orm)
            self.session.commit()
            self.session.refresh(book_orm)
            book.book_id = book_orm.book_id
            return f"Book '{book.title}' added successfully"
        except IntegrityError:
            self.session.rollback()
            raise DuplicateError("Book", book.title)
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def remove_book(self, book_id):
       
        if not book_id or not isinstance(book_id, int):
            raise ValueError("Book ID must be a valid integer")

        try:
            stmt = select(BookORM).where(BookORM.book_id == book_id)
            book_obj = self.session.execute(stmt).scalar_one_or_none()
            if book_obj is None:
                logger.warning("Book not found for removal book_id=%s", book_id)
                raise NotFoundError("Book", book_id)
            self.session.delete(book_obj)
            self.session.commit()
            logger.info("Removed book book_id=%s", book_id)
            return "Book removed successfully"
        except SQLAlchemyError:
            self.session.rollback()
            logger.exception("Database error while removing book book_id=%s", book_id)
            raise

    def register_user(self, user):
       
        if not user or not user.name:
            raise ValueError("User object must have a name")

        try:
            logger.info("Registering user object name=%s", user.name)
            user_orm = UserORM(name=user.name, borrow_limit=user.borrow_limit, borrow_days=user.borrow_days, fine_per_day=user.fine_per_day)
            self.session.add(user_orm)
            self.session.commit()
            self.session.refresh(user_orm)
            user.user_id = user_orm.user_id
            return f"User '{user.name}' registered"
        except IntegrityError:
            self.session.rollback()
            logger.warning("Duplicate user detected while registering name=%s", user.name)
            raise DuplicateError("User", user.name)
        except SQLAlchemyError:
            self.session.rollback()
            logger.exception("Database error while registering user name=%s", user.name)
            raise

    def display_books(self):
        try:
            stmt = select(BookORM).order_by(BookORM.book_id)
            results = self.session.execute(stmt).scalars().all()

            if not results:
                return "No books found"

            output = []
            for book in results:
                status = "Available" if book.available else "Borrowed"
                output.append(
                    f"ID: {book.book_id}\n"
                    f"Title: {book.title}\n"
                    f"Author: {book.author}\n"
                    f"Status: {status}"
                )

            return "\n\n".join(output)
        except SQLAlchemyError:
            raise

    def display_users(self):
        try:
            stmt = select(UserORM).order_by(UserORM.user_id)
            users = self.session.execute(stmt).scalars().all()

            if not users:
                return "No registered users."

            output = []
            for user_row in users:
                user = User(
                    user_row.user_id,
                    user_row.name,
                    borrow_limit=user_row.borrow_limit,
                    borrow_days=user_row.borrow_days,
                    fine_per_day=float(user_row.fine_per_day),
                )
                user.borrowed_books = self._get_active_borrowed_books(user.user_id)
                output.append(user.display_details())

            return "\n\n".join(output)
        except SQLAlchemyError:
            raise

    def lend_book(self, book_id, user_id):
       
        if not book_id or not isinstance(book_id, int):
            raise ValueError("Book ID must be a valid integer")
        if not user_id or not isinstance(user_id, int):
            raise ValueError("User ID must be a valid integer")

        try:
            logger.info("Lending book book_id=%s to user_id=%s", book_id, user_id)
            book_obj = self._find_book_orm(book_id)
            if book_obj is None:
                logger.warning("Book not found while lending book_id=%s", book_id)
                raise NotFoundError("Book", book_id)

            if not book_obj.available:
                logger.warning("Attempted to lend unavailable book book_id=%s", book_id)
                raise ValidationError(f"'{book_obj.title}' is not available right now")

            user = self._find_user(user_id)
            if user is None:
                logger.warning("User not found while lending user_id=%s", user_id)
                raise NotFoundError("User", user_id)

            active_count = self._get_active_borrow_count(user_id)
            if active_count >= user.borrow_limit:
                logger.warning("Borrow limit reached user_id=%s", user_id)
                raise ValidationError(f"Borrow limit reached ({user.borrow_limit} books)")

            borrowed_date = date.today()
            due_date = borrowed_date + timedelta(days=user.borrow_days)

            entry = BorrowHistoryORM(user_id=user_id, book_id=book_id, borrowed_on=borrowed_date, due_on=due_date, returned_on=None, fine=0.00)
            book_obj.available = False
            self.session.add(entry)
            self.session.commit()
            logger.info("Book lent successfully book_id=%s user_id=%s due=%s", book_id, user_id, due_date)

            return f"{user.name} borrowed {book_obj.title}. Due on {due_date}."
        except SQLAlchemyError:
            self.session.rollback()
            logger.exception("Database error while lending book_id=%s user_id=%s", book_id, user_id)
            raise

    def accept_return(self, book_id, user_id):
      
        if not book_id or not isinstance(book_id, int):
            raise ValueError("Book ID must be a valid integer")
        if not user_id or not isinstance(user_id, int):
            raise ValueError("User ID must be a valid integer")

        try:
            logger.info("Accepting return book_id=%s user_id=%s", book_id, user_id)
            book_obj = self._find_book_orm(book_id)
            if book_obj is None:
                logger.warning("Book not found while returning book_id=%s", book_id)
                raise NotFoundError("Book", book_id)

            user = self._find_user(user_id)
            if user is None:
                logger.warning("User not found while returning user_id=%s", user_id)
                raise NotFoundError("User", user_id)

            stmt = (
                select(BorrowHistoryORM)
                .where(
                    BorrowHistoryORM.user_id == user_id,
                    BorrowHistoryORM.book_id == book_id,
                    BorrowHistoryORM.returned_on.is_(None),
                )
                .order_by(BorrowHistoryORM.borrowed_on.desc())
            )
            borrow_row = self.session.execute(stmt).scalars().first()
            if borrow_row is None:
                logger.warning("No active borrow found book_id=%s user_id=%s", book_id, user_id)
                raise ValidationError(f"{user.name} has not borrowed {book_obj.title}")

            fine_per_day = float(user.fine_per_day) if hasattr(user, "fine_per_day") else 2.0

            today = date.today()
            late_days = max((today - borrow_row.due_on).days, 0)
            fine = late_days * fine_per_day

            borrow_row.returned_on = today
            borrow_row.fine = fine
            book_obj.available = True
            self.session.commit()
            logger.info("Book returned successfully book_id=%s user_id=%s fine=%.2f", book_id, user_id, fine)

            if fine > 0:
                return f"{user.name} returned {book_obj.title}. Late by {late_days} days. Fine: {fine:.2f}."

            return f"{user.name} returned {book_obj.title}. No fine."
        except SQLAlchemyError:
            self.session.rollback()
            logger.exception("Database error while accepting return book_id=%s user_id=%s", book_id, user_id)
            raise

    def display_available_books(self):

        try:
            stmt = select(BookORM).where(BookORM.available.is_(True)).order_by(BookORM.book_id)
            books = self.session.execute(stmt).scalars().all()

            if not books:
                return "No available books."

            output = []
            for book in books:
                output.append(Book(book.book_id, book.title, book.author, book.available).display_details())

            return "\n\n".join(output)
        except SQLAlchemyError:
            raise

    def search_books(self, query_text):
       
        if not query_text or not query_text.strip():
            raise ValueError("Search query cannot be empty")

        try:
            search_pattern = f"%{query_text}%"
            stmt = select(BookORM).where(
                or_(BookORM.title.ilike(search_pattern), BookORM.author.ilike(search_pattern))
            ).order_by(BookORM.book_id)
            books = self.session.execute(stmt).scalars().all()

            if not books:
                return "No books found"

            output = [f"{b.title} by {b.author}" for b in books]
            return "\n".join(output)
        except SQLAlchemyError:
            raise

    def display_user_borrow_history(self, user_id):
        
        if not user_id or not isinstance(user_id, int):
            raise ValueError("User ID must be a valid integer")

        try:
            user = self._find_user(user_id)
            if user is None:
                raise NotFoundError("User", user_id)

            stmt = (
                select(BorrowHistoryORM, BookORM)
                .join(BookORM, BorrowHistoryORM.book_id == BookORM.book_id)
                .where(BorrowHistoryORM.user_id == user_id)
                .order_by(BorrowHistoryORM.borrowed_on.desc())
            )
            rows = self.session.execute(stmt).all()

            if not rows:
                return f"No borrow history for {user.name}."

            lines = []
            for bh, b in rows:
                returned_on = bh.returned_on if bh.returned_on is not None else "Not returned"
                lines.append(
                    f"Book ID: {b.book_id} | Title: {b.title} | "
                    f"Borrowed: {bh.borrowed_on} | Due: {bh.due_on} | "
                    f"Returned: {returned_on} | Fine: {float(bh.fine):.2f}"
                )

            return "\n".join(lines)
        except SQLAlchemyError:
            raise

    def _find_book(self, book_id):
        stmt = select(BookORM).where(BookORM.book_id == book_id)
        book_row = self.session.execute(stmt).scalars().first()
        if book_row is None:
            return None
        return Book(book_row.book_id, book_row.title, book_row.author, book_row.available)

    def _find_user(self, user_id):
       
        stmt = select(UserORM).where(UserORM.user_id == user_id)
        user_row = self.session.execute(stmt).scalars().first()
        if user_row is None:
            return None

        user = User(
            user_row.user_id,
            user_row.name,
            borrow_limit=user_row.borrow_limit,
            borrow_days=user_row.borrow_days,
            fine_per_day=float(user_row.fine_per_day),
        )
        user.borrowed_books = self._get_active_borrowed_books(user_id)
        user.fine_per_day = float(user_row.fine_per_day)
        return user

    def _get_active_borrow_count(self, user_id):
        stmt = select(func.count()).select_from(BorrowHistoryORM).where(
            BorrowHistoryORM.user_id == user_id, BorrowHistoryORM.returned_on.is_(None)
        )
        count = self.session.execute(stmt).scalar_one()
        return count

    def _get_active_borrowed_books(self, user_id):
       
        stmt = (
            select(BookORM)
            .join(BorrowHistoryORM, BorrowHistoryORM.book_id == BookORM.book_id)
            .where(BorrowHistoryORM.user_id == user_id, BorrowHistoryORM.returned_on.is_(None))
            .order_by(BorrowHistoryORM.borrowed_on.desc())
        )
        books = [Book(b.book_id, b.title, b.author, b.available) for b in self.session.execute(stmt).scalars().all()]
        return books

    def _get_due_date(self, user_id, book_id):
        stmt = (
            select(BorrowHistoryORM.due_on)
            .where(
                BorrowHistoryORM.user_id == user_id,
                BorrowHistoryORM.book_id == book_id,
                BorrowHistoryORM.returned_on.is_(None),
            )
            .order_by(BorrowHistoryORM.borrowed_on.desc())
            .limit(1)
        )
        due_row = self.session.execute(stmt).scalars().first()
        due_date = due_row if due_row else "Unknown"
        return due_date

   
    def _find_book_orm(self, book_id):
        stmt = select(BookORM).where(BookORM.book_id == book_id)
        return self.session.execute(stmt).scalars().first()
