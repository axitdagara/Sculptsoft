from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, examples=["Aarav"])


class UserCreate(UserBase):
    borrow_limit: int = Field(default=3, ge=1, le=10)
    borrow_days: int = Field(default=14, ge=1, le=60)
    fine_per_day: Decimal = Field(default=Decimal("2.00"), ge=0)


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    borrow_limit: int | None = Field(default=None, ge=1, le=10)
    borrow_days: int | None = Field(default=None, ge=1, le=60)
    fine_per_day: Decimal | None = Field(default=None, ge=0)


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    borrow_limit: int
    borrow_days: int
    fine_per_day: Decimal
