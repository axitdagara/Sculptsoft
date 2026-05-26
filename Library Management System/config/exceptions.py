class ConnectionException(Exception):
    """Raised when the database connection cannot be established."""
    pass


class DatabaseException(Exception):
    """Raised when a database operation fails."""
    pass


class BookNotFoundException(Exception):
    """Raised when a book cannot be found."""
    pass


class UserNotFoundException(Exception):
    """Raised when a user cannot be found."""
    pass


class BorrowLimitExceededException(Exception):
    """Raised when a user reaches the borrow limit."""
    pass


class BookNotAvailableException(Exception):
    """Raised when a book is already borrowed."""
    pass


class InvalidBorrowException(Exception):
    """Raised when a borrow operation fails."""
    pass


class InvalidReturnException(Exception):
    """Raised when a return operation fails."""
    pass
