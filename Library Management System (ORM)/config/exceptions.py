
from typing import Any, Optional


class ApplicationError(Exception):  
    pass


class NotFoundError(ApplicationError):  
    
    def __init__(self, entity: str, identifier: Optional[Any] = None):
        self.entity = entity
        self.identifier = identifier
        message = f"{entity} not found"
        if identifier is not None:
            message += f": {identifier}"
        super().__init__(message)


class ValidationError(ApplicationError):
    
    def __init__(self, message: str, field: Optional[str] = None):
        self.field = field
        super().__init__(message)


class DuplicateError(ApplicationError):

    def __init__(self, entity: str, identifier: Optional[Any] = None):
        self.entity = entity
        self.identifier = identifier
        message = f"Duplicate {entity}"
        if identifier is not None:
            message += f": {identifier}"
        super().__init__(message)


class DatabaseError(ApplicationError):

    def __init__(self, message: str = "An error occurred with the database"):
        super().__init__(message)
