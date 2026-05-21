from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate, UserResponse
import crud, models
from database import engine

models.Base.metadata.create_all(bind=engine)  # tables banao

app = FastAPI()

# GET — sab users
@app.get("/users/", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

# GET — ek user by ID
@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User nahi mila!")
    return user

# POST — naya user banao
@app.post("/users/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

# DELETE — user hatao
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.delete_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User nahi mila!")
    return {"message": "User delete ho gaya"}