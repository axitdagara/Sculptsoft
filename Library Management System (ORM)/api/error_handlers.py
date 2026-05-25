from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from config.exceptions import ApplicationError, DatabaseError, DuplicateError, NotFoundError, ValidationError
from config.logger import get_logger


logger = get_logger(__name__)


def _json_error(status_code: int, error_name: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": error_name, "message": message},
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def handle_not_found(_: Request, exc: NotFoundError) -> JSONResponse:
        return _json_error(404, "NotFoundError", str(exc))

    @app.exception_handler(DuplicateError)
    async def handle_duplicate(_: Request, exc: DuplicateError) -> JSONResponse:
        return _json_error(409, "DuplicateError", str(exc))

    @app.exception_handler(ValidationError)
    async def handle_validation(_: Request, exc: ValidationError) -> JSONResponse:
        return _json_error(400, "ValidationError", str(exc))

    @app.exception_handler(DatabaseError)
    async def handle_database(_: Request, exc: DatabaseError) -> JSONResponse:
        logger.exception("Database error handled by API")
        return _json_error(500, "DatabaseError", str(exc))

    @app.exception_handler(ApplicationError)
    async def handle_application(_: Request, exc: ApplicationError) -> JSONResponse:
        return _json_error(400, "ApplicationError", str(exc))

    @app.exception_handler(SQLAlchemyError)
    async def handle_sqlalchemy(_: Request, exc: SQLAlchemyError) -> JSONResponse:
        logger.exception("Unhandled SQLAlchemy error")
        return _json_error(500, "DatabaseError", "Unexpected database failure")

    @app.exception_handler(RequestValidationError)
    async def handle_request_validation(_: Request, exc: RequestValidationError) -> JSONResponse:
        details = [
            {
                "field": ".".join([str(x) for x in error.get("loc", [])]),
                "message": error.get("msg", "Invalid value"),
            }
            for error in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            content={
                "error": "RequestValidationError",
                "message": "Request body/query/path validation failed",
                "details": details,
            },
        )

    @app.exception_handler(Exception)
    async def handle_unexpected(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unexpected API error", exc_info=exc)
        return _json_error(500, "InternalServerError", "Something went wrong")
