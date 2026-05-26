from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, get_db, Base
from .config import settings
from .logger import get_logger

Base.metadata.create_all(bind=engine)

logger = get_logger()

app = FastAPI(title="Library Management System")


@app.post("/books/", response_model=schemas.BookOut)
def create_book(book_in: schemas.BookCreate, db: Session = Depends(get_db)):
    book = crud.add_book(db, book_in.title, book_in.author)
    logger.info(f"Book added: {book.title} by {book.author}")
    return book


@app.delete("/books/{book_id}", response_model=schemas.BookOut)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    try:
        book = crud.remove_book(db, book_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    logger.info(f"Book removed: {book.title}")
    return book


@app.post("/users/", response_model=schemas.UserOut)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.register_user(db, user_in.name)
    logger.info(f"User registered: {user.name}")
    return user


@app.post("/lend/{book_id}/to/{user_id}", response_model=schemas.BorrowOut)
def lend(book_id: int, user_id: int, db: Session = Depends(get_db)):
    try:
        borrow = crud.lend_book(db, book_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    logger.info(f"Book {book_id} lent to user {user_id}")
    return borrow


@app.post("/return/{book_id}/from/{user_id}", response_model=schemas.BorrowOut)
def return_book(book_id: int, user_id: int, db: Session = Depends(get_db)):
    try:
        borrow = crud.accept_return(db, book_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    logger.info(f"Book {book_id} returned by user {user_id}")
    return borrow


@app.get("/books/available", response_model=list[schemas.BookOut])
def available_books(db: Session = Depends(get_db)):
    return crud.list_available(db)


@app.get("/books/search", response_model=list[schemas.BookOut])
def search(q: str, db: Session = Depends(get_db)):
    return crud.search_books(db, q)


@app.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # build borrowed_books list
    borrowed = [b.book for b in user.borrows if b.return_date is None]
    return {"id": user.id, "name": user.name, "borrowed_books": borrowed}
