from pathlib import Path

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import FileResponse

from exceptions import UnauthorizedError
from models.orm_models import UserORM
from schemas import BorrowActionResponse, BorrowHistoryRead, ErrorResponse
from services.auth import get_current_user

from .dependencies import get_library


protected_router = APIRouter(prefix="/api/v1", dependencies=[Depends(get_current_user)])
public_router = APIRouter()
REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"


@protected_router.post(
    "/borrow",
    response_model=BorrowActionResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Borrowing"],
    summary="Borrow a book",
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def borrow_book(
    user_id: int = Body(..., ge=1),
    book_id: int = Body(..., ge=1),
    current_user: UserORM = Depends(get_current_user),
    library=Depends(get_library),
):
    if current_user.role != "admin" and user_id != current_user.user_id:
        raise UnauthorizedError("You can only borrow books for your own account")
    return library.borrow_book(user_id, book_id)


@protected_router.post(
    "/return",
    response_model=BorrowActionResponse,
    status_code=status.HTTP_200_OK,
    tags=["Borrowing"],
    summary="Return a book",
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def return_book(
    user_id: int = Body(..., ge=1),
    book_id: int = Body(..., ge=1),
    current_user: UserORM = Depends(get_current_user),
    library=Depends(get_library),
):
    if current_user.role != "admin" and user_id != current_user.user_id:
        raise UnauthorizedError("You can only return books for your own account")
    return library.return_book(user_id, book_id)


@protected_router.get(
    "/users/{user_id}/borrow-history",
    response_model=list[BorrowHistoryRead],
    status_code=status.HTTP_200_OK,
    tags=["Borrowing"],
    summary="Get a user's borrow history",
    responses={404: {"model": ErrorResponse}},
)
def get_user_borrow_history(
    user_id: int,
    current_user: UserORM = Depends(get_current_user),
    library=Depends(get_library),
):
    if current_user.role != "admin" and user_id != current_user.user_id:
        raise UnauthorizedError("You can only view your own borrow history")
    return library.get_user_borrow_history(user_id)


@protected_router.post(
    "/reports/overdue-summary",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Reports"],
    summary="Generate overdue report (Async)",
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def generate_overdue_report(
    current_user: UserORM = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise UnauthorizedError("Only admins can generate reports")

    from config.library_tasks import generate_report_task
    task = generate_report_task.delay()
    return {"task_id": task.id, "message": "Report generation started"}


@public_router.get(
    "/reports/download/{file_name}",
    tags=["Reports"],
    summary="Download generated report",
    responses={404: {"model": ErrorResponse}},
)
def download_report(file_name: str):
    if file_name != "overdue.pdf":
        raise HTTPException(status_code=404, detail="Report not found")

    report_path = REPORTS_DIR / file_name
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Report not generated yet")

    return FileResponse(
        report_path,
        media_type="application/pdf",
        filename=file_name,
    )
