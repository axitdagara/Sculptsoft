from fastapi import APIRouter, Body, Depends, Response, status

from schemas import BookRead, ErrorResponse
from services.auth import get_current_user

from .dependencies import get_library


protected_router = APIRouter(prefix="/api/v1", dependencies=[Depends(get_current_user)])


@protected_router.get(
    "/books",
    response_model=list[BookRead],
    status_code=status.HTTP_200_OK,
    tags=["Books"],
    summary="List all books",
)
async def list_books(library=Depends(get_library)):
    return library.list_books()


@protected_router.post(
    "/books",
    response_model=BookRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Books"],
    summary="Create a new book",
    responses={400: {"model": ErrorResponse}, 409: {"model": ErrorResponse}},
)
async def create_book(
    title: str = Body(..., min_length=1, max_length=255),
    author: str = Body(..., min_length=1, max_length=255),
    library=Depends(get_library),
):
    return library.create_book(title, author)


@protected_router.get(
    "/books/{book_id}",
    response_model=BookRead,
    status_code=status.HTTP_200_OK,
    tags=["Books"],
    summary="Get a single book by ID",
    responses={404: {"model": ErrorResponse}},
)
async def get_book(book_id: int, library=Depends(get_library)):
    return library.get_book(book_id)


@protected_router.put(
    "/books/{book_id}",
    response_model=BookRead,
    status_code=status.HTTP_200_OK,
    tags=["Books"],
    summary="Update a book",
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
async def update_book(
    book_id: int,
    title: str | None = Body(default=None, min_length=1, max_length=255),
    author: str | None = Body(default=None, min_length=1, max_length=255),
    available: bool | None = Body(default=None),
    library=Depends(get_library),
):
    return library.update_book(book_id, title=title, author=author, available=available)


@protected_router.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Books"],
    summary="Delete a book",
    responses={404: {"model": ErrorResponse}},
)
async def delete_book(book_id: int, library=Depends(get_library)):
    library.delete_book(book_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
