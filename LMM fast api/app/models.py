from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from .database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, index=True, nullable=False)
    available = Column(Boolean, default=True, nullable=False)

    borrows = relationship("Borrow", back_populates="book")

    def display_details(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "available": self.available,
        }


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    borrows = relationship("Borrow", back_populates="user")


class Borrow(Base):
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=14))
    return_date = Column(DateTime, nullable=True)
    fine = Column(Float, default=0.0)

    user = relationship("User", back_populates="borrows")
    book = relationship("Book", back_populates="borrows")
