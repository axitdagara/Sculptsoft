from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class BookCreate(BaseModel):
    title: str
    author: str


class BookOut(BaseModel):
    id: int
    title: str
    author: str
    available: bool

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str


class UserOut(BaseModel):
    id: int
    name: str
    borrowed_books: List[BookOut] = []

    class Config:
        orm_mode = True


class BorrowOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime]
    fine: float

    class Config:
        orm_mode = True
