"""
Common application exceptions for the Library Management System.

Move project-wide exceptions here and import from `config.exceptions`.
"""
from typing import Any, Optional


class ApplicationError(Exception):
    """Base class for all custom exceptions in the application."""


class NotFoundError(ApplicationError):
    """Raised when a requested entity cannot be found."""

    def __init__(self, entity: str, identifier: Optional[Any] = None):
        self.entity = entity
        self.identifier = identifier
        message = f"{entity} not found"
        if identifier is not None:
            message += f": {identifier}"
        super().__init__(message)


class ValidationError(ApplicationError):
    """Raised when input/data validation fails."""

    def __init__(self, message: str, field: Optional[str] = None):
        self.field = field
        super().__init__(message)


class DuplicateError(ApplicationError):
    """Raised when attempting to create a duplicate resource."""

    def __init__(self, entity: str, identifier: Optional[Any] = None):
        self.entity = entity
        self.identifier = identifier
        message = f"Duplicate {entity}"
        if identifier is not None:
            message += f": {identifier}"
        super().__init__(message)


class DatabaseError(ApplicationError):
    """Raised for general database-related errors."""

    def __init__(self, message: str = "An error occurred with the database"):
        super().__init__(message)
