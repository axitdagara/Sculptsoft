from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, examples=["Clean Code"])
    author: str = Field(..., min_length=1, max_length=255, examples=["Robert C. Martin"])


class BookRead(BookBase):
    model_config = ConfigDict(from_attributes=True)

    book_id: int
    available: bool
