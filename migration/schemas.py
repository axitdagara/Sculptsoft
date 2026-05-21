from pydantic import BaseModel, EmailStr

# User banate waqt kya input chahiye
class UserCreate(BaseModel):
    name: str
    email: EmailStr 

# Response mein kya return karein
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True  # ORM object → dict conversion