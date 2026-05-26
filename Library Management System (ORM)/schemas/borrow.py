from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_serializer


class BorrowActionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    message: str
    user_id: int
    book_id: int
    book_title: str
    borrowed_on: date | None = None
    due_on: date | None = None
    returned_on: date | None = None
    fine: Decimal = Decimal("0.00")

    @field_serializer("fine")
    def serialize_fine(self, value: Decimal) -> str:
        return f"{value:.2f}"


class BorrowHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    history_id: int
    user_id: int
    book_id: int
    book_title: str
    book_author: str
    borrowed_on: date
    due_on: date
    returned_on: date | None
    fine: Decimal

    @field_serializer("fine")
    def serialize_fine(self, value: Decimal) -> str:
        return f"{value:.2f}"