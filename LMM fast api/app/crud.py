from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from . import models
from .config import settings
from datetime import datetime


def add_book(db: Session, title: str, author: str):
    book = models.Book(title=title, author=author, available=True)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def remove_book(db: Session, book_id: int):
    book = db.get(models.Book, book_id)
    if not book:
        return None
    if any(b.return_date is None for b in book.borrows):
        raise ValueError("Book is currently borrowed")
    db.delete(book)
    db.commit()
    return book


def register_user(db: Session, name: str):
    user = models.User(name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def lend_book(db: Session, book_id: int, user_id: int):
    book = db.get(models.Book, book_id)
    user = db.get(models.User, user_id)
    if not book:
        raise ValueError("Book not found")
    if not user:
        raise ValueError("User not found")
    if not book.available:
        raise ValueError("Book not available")

    # enforce borrow limit
    active_borrows = [b for b in user.borrows if b.return_date is None]
    if len(active_borrows) >= settings.borrow_limit:
        raise ValueError("User reached borrow limit")

    borrow = models.Borrow(user_id=user.id, book_id=book.id)
    book.available = False
    db.add(borrow)
    db.commit()
    db.refresh(borrow)
    return borrow


def accept_return(db: Session, book_id: int, user_id: int):
    stmt = select(models.Borrow).where(
        and_(models.Borrow.book_id == book_id, models.Borrow.user_id == user_id, models.Borrow.return_date == None)
    )
    borrow = db.execute(stmt).scalars().first()
    if not borrow:
        raise ValueError("Active borrow not found")
    borrow.return_date = datetime.utcnow()
    # compute fine
    if borrow.return_date > borrow.due_date:
        days = (borrow.return_date - borrow.due_date).days
        borrow.fine = days * settings.fine_per_day
    borrow.book.available = True
    db.add(borrow)
    db.commit()
    db.refresh(borrow)
    return borrow


def list_available(db: Session):
    stmt = select(models.Book).where(models.Book.available == True)
    return db.execute(stmt).scalars().all()


def search_books(db: Session, q: str):
    q_lower = f"%{q}%"
    stmt = select(models.Book).where(
        models.Book.title.ilike(q_lower) | models.Book.author.ilike(q_lower)
    )
    return db.execute(stmt).scalars().all()
