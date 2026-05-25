from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, examples=["Clean Code"])
    author: str = Field(..., min_length=1, max_length=255, examples=["Robert C. Martin"])


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    author: str | None = Field(default=None, min_length=1, max_length=255)
    available: bool | None = None


class BookRead(BookBase):
    model_config = ConfigDict(from_attributes=True)

    book_id: int
    available: bool
