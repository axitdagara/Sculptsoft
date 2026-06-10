import time
from datetime import date
from pathlib import Path

from config.celery_app import celery_app
from config.logger import get_logger
from config.db import get_session
from models.orm_models import BookORM, BorrowHistoryORM, UserORM

logger = get_logger(__name__)
REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
OVERDUE_REPORT_PATH = REPORTS_DIR / "overdue.pdf"


def _escape_pdf_text(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _write_simple_pdf(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    text_commands = ["BT", "/F1 11 Tf", "50 790 Td", "14 TL"]
    for line in lines:
        text_commands.append(f"({_escape_pdf_text(line)}) Tj")
        text_commands.append("T*")
    text_commands.append("ET")
    content = "\n".join(text_commands).encode("latin-1", errors="replace")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(content)).encode("ascii") + b" >>\nstream\n" + content + b"\nendstream",
    ]

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{index} 0 obj\n".encode("ascii"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    )

    path.write_bytes(pdf)

@celery_app.task
def send_borrow_confirmation_email(user_name: str, book_title: str, due_on: str):
    logger.info("Sending borrow confirmation to %s for '%s'. Due: %s", user_name, book_title, due_on)
    return True

@celery_app.task
def send_return_confirmation_email(user_name: str, book_title: str, fine: str):
    logger.info("Sending return confirmation to %s for '%s'. Fine: %s", user_name, book_title, fine)
    return True

@celery_app.task
def send_overdue_notifications():
    # Utilizing a distinct DB session for background scheduled jobs
    db = get_session()
    try:
        today = date.today()
        overdue_borrows = (
            db.query(BorrowHistoryORM)
            .filter(
                BorrowHistoryORM.returned_on.is_(None),
                BorrowHistoryORM.due_on < today
            )
            .all()
        )
        for borrow in overdue_borrows:
            user = borrow.user
            book = borrow.book
            # Here you would integrate with an email/SMS provider
            logger.info(
                "Overdue Notification: User %s has not returned '%s'. Due date was %s", 
                user.name, book.title, borrow.due_on
            )
    finally:
        db.close()

@celery_app.task
def generate_report_task():
    logger.info("Starting report generation...")
    db = get_session()
    try:
        today = date.today()
        overdue_borrows = (
            db.query(BorrowHistoryORM, UserORM, BookORM)
            .join(UserORM, BorrowHistoryORM.user_id == UserORM.user_id)
            .join(BookORM, BorrowHistoryORM.book_id == BookORM.book_id)
            .filter(
                BorrowHistoryORM.returned_on.is_(None),
                BorrowHistoryORM.due_on < today,
            )
            .order_by(BorrowHistoryORM.due_on.asc(), BorrowHistoryORM.history_id.asc())
            .all()
        )

        lines = [
            "Library Management System",
            f"Overdue Report - {today.isoformat()}",
            "",
        ]
        if not overdue_borrows:
            lines.append("No overdue books found.")
        else:
            lines.append("User | Book | Borrowed On | Due On | Days Overdue")
            for history, user, book in overdue_borrows:
                days_overdue = (today - history.due_on).days
                lines.append(
                    f"{user.name} | {book.title} | {history.borrowed_on} | {history.due_on} | {days_overdue}"
                )

        _write_simple_pdf(OVERDUE_REPORT_PATH, lines)
    finally:
        db.close()

    time.sleep(1)
    logger.info("Report generation completed.")
    return {"status": "success", "report_url": "http://localhost:8000/reports/download/overdue.pdf"}
