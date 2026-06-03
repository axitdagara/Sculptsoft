

import logging
from typing import Any, Optional

from fastapi import HTTPException


logger = logging.getLogger("exceptions")


class ApplicationError(HTTPException):
    def __init__(self, status_code: int = 400, detail: str | None = None):
        super().__init__(status_code=status_code, detail=detail or "Application error")


class NotFoundError(ApplicationError):
    def __init__(self, entity: str, identifier: Optional[Any] = None):
        message = f"{entity} not found"
        if identifier is not None:
            message += f": {identifier}"
        super().__init__(status_code=404, detail=message)


class ValidationError(ApplicationError):
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(status_code=400, detail=message)


class DuplicateError(ApplicationError):
    def __init__(self, entity: str, identifier: Optional[Any] = None):
        message = f"Duplicate {entity}"
        if identifier is not None:
            message += f": {identifier}"
        super().__init__(status_code=409, detail=message)


class DatabaseError(ApplicationError):
    def __init__(self, message: str = "An error occurred with the database"):
        super().__init__(status_code=500, detail=message)


class UnauthorizedError(ApplicationError):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(status_code=401, detail=message)


class ForbiddenError(ApplicationError):
    def __init__(self, message: str = "You do not have permission to access this resource"):
        super().__init__(status_code=403, detail=message)
