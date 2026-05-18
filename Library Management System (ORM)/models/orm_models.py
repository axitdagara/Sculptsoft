from sqlalchemy import Column, Integer, String, Boolean, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base


class BookORM(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    available = Column(Boolean, nullable=False, default=True)

    borrow_entries = relationship("BorrowHistoryORM", back_populates="book", cascade="all, delete-orphan")


class UserORM(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    borrow_limit = Column(Integer, nullable=False, default=3)
    borrow_days = Column(Integer, nullable=False, default=14)
    fine_per_day = Column(Numeric(10, 2), nullable=False, default=2.00)

    borrow_entries = relationship("BorrowHistoryORM", back_populates="user", cascade="all, delete-orphan")


class BorrowHistoryORM(Base):
    __tablename__ = "borrow_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.book_id", ondelete="CASCADE"), nullable=False)
    borrowed_on = Column(Date, nullable=False)
    due_on = Column(Date, nullable=False)
    returned_on = Column(Date, nullable=True)
    fine = Column(Numeric(10, 2), nullable=False, default=0.00)

    user = relationship("UserORM", back_populates="borrow_entries")
    book = relationship("BookORM", back_populates="borrow_entries")
