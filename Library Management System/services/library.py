import logging
from config.db import create_connection
from config.exceptions import (
    ConnectionException,
    DatabaseException,
    BookNotFoundException,
    UserNotFoundException,
    BorrowLimitExceededException,
    BookNotAvailableException,
    InvalidBorrowException,
    InvalidReturnException,
)
from models.book import Book
from models.user import User

logger = logging.getLogger(__name__)


class Library:
    def __init__(self):
        """Initialize the Library with database connection."""
        try:
            logger.info("Initializing Library...")
            self.connection = create_connection()
            if self.connection is None:
                raise ConnectionException("Database connection could not be established.")
            
            self.cursor = self.connection.cursor()
            logger.debug("Database cursor created successfully")
            
            self._ensure_tables()
            logger.info("Library initialized successfully")
        except ConnectionException as e:
            logger.error(f"Connection failed during Library initialization: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during Library initialization: {str(e)}")
            raise ConnectionException(f"Failed to initialize Library: {str(e)}") from e

    def _ensure_tables(self):
        """Create required database tables if they don't exist."""
        try:
            logger.debug("Ensuring database tables exist...")
            
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS books (
                    book_id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    author VARCHAR(255) NOT NULL,
                    available BOOLEAN NOT NULL DEFAULT TRUE
                )
                """
            )
            logger.debug("Books table created/verified")
            
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    borrow_limit INTEGER NOT NULL DEFAULT 3,
                    borrow_days INTEGER NOT NULL DEFAULT 14,
                    fine_per_day NUMERIC(10, 2) NOT NULL DEFAULT 2.00
                )
                """
            )
            logger.debug("Users table created/verified")
            
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS borrow_history (
                    history_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                    book_id INTEGER NOT NULL REFERENCES books(book_id) ON DELETE CASCADE,
                    borrowed_on DATE NOT NULL,
                    due_on DATE NOT NULL,
                    returned_on DATE,
                    fine NUMERIC(10, 2) NOT NULL DEFAULT 0.00
                )
                """
            )
            logger.debug("Borrow history table created/verified")
            
            self.connection.commit()
            logger.info("All database tables verified/created successfully")
        except Exception as e:
            logger.error(f"Failed to ensure tables: {str(e)}")
            self.connection.rollback()
            raise DatabaseException(f"Failed to create/verify database tables: {str(e)}") from e

    def create_book(self, title, author):
        """Create and add a new book to the library."""
        try:
            if not title or not title.strip():
                logger.warning("Attempt to create book with empty title")
                raise ValueError("Book title cannot be empty")
            if not author or not author.strip():
                logger.warning("Attempt to create book with empty author")
                raise ValueError("Book author cannot be empty")
            
            logger.debug(f"Creating book: '{title}' by '{author}'")
            
            query = """
            INSERT INTO books (title, author, available)
            VALUES (%s, %s, %s)
            RETURNING book_id
            """
            self.cursor.execute(query, (title, author, True))
            book_id = self.cursor.fetchone()[0]
            self.connection.commit()
            
            logger.info(f"Book created successfully with ID: {book_id}, Title: '{title}'")
            return Book(book_id, title, author, True)
        except ValueError as e:
            logger.error(f"Validation error while creating book: {str(e)}")
            self.connection.rollback()
            raise
        except Exception as e:
            logger.error(f"Database error while creating book: {str(e)}")
            self.connection.rollback()
            raise DatabaseException(f"Failed to create book: {str(e)}") from e

    def create_user(self, name):
        """Create and register a new user in the library."""
        try:
            if not name or not name.strip():
                logger.warning("Attempt to create user with empty name")
                raise ValueError("User name cannot be empty")
            
            logger.debug(f"Creating user: '{name}'")
            
            query = """
            INSERT INTO users (name, borrow_limit, borrow_days, fine_per_day)
            VALUES (%s, %s, %s, %s)
            RETURNING user_id
            """
            self.cursor.execute(query, (name, 3, 14, 2.0))
            user_id = self.cursor.fetchone()[0]
            self.connection.commit()
            
            logger.info(f"User created successfully with ID: {user_id}, Name: '{name}'")
            return User(user_id, name)
        except ValueError as e:
            logger.error(f"Validation error while creating user: {str(e)}")
            self.connection.rollback()
            raise
        except Exception as e:
            logger.error(f"Database error while creating user: {str(e)}")
            self.connection.rollback()
            raise DatabaseException(f"Failed to create user: {str(e)}") from e

    def add_book(self, book):
        """Add an existing book object to the library."""
        try:
            if not book or not book.title or not book.author:
                logger.warning("Attempt to add invalid book object")
                raise ValueError("Book object must have title and author")
            
            logger.debug(f"Adding book: '{book.title}' by '{book.author}'")
            
            query = """
            INSERT INTO books (title, author, available)
            VALUES (%s, %s, %s)
            RETURNING book_id
            """
            self.cursor.execute(query, (book.title, book.author, book.available))
            book.book_id = self.cursor.fetchone()[0]
            self.connection.commit()
            
            logger.info(f"Book added successfully: ID={book.book_id}, Title='{book.title}'")
            return f"Book '{book.title}' added successfully"
        except ValueError as e:
            logger.error(f"Validation error while adding book: {str(e)}")
            self.connection.rollback()
            raise
        except Exception as e:
            logger.error(f"Database error while adding book: {str(e)}")
            self.connection.rollback()
            raise DatabaseException(f"Failed to add book: {str(e)}") from e

    def remove_book(self, book_id):
        """Remove a book from the library by its ID."""
        try:
            if not book_id or not isinstance(book_id, int):
                logger.warning(f"Invalid book_id for removal: {book_id}")
                raise ValueError("Book ID must be a valid integer")
            
            logger.debug(f"Removing book with ID: {book_id}")
            
            query = "DELETE FROM books WHERE book_id = %s"
            self.cursor.execute(query, (book_id,))
            self.connection.commit()

            if self.cursor.rowcount == 0:
                logger.warning(f"Book not found for removal: ID={book_id}")
                raise BookNotFoundException(f"Book with ID {book_id} not found")
            
            logger.info(f"Book removed successfully: ID={book_id}")
            return "Book removed successfully"
        except (ValueError, BookNotFoundException) as e:
            logger.error(f"Error removing book: {str(e)}")
            self.connection.rollback()
            raise
        except Exception as e:
            logger.error(f"Database error while removing book: {str(e)}")
            self.connection.rollback()
            raise DatabaseException(f"Failed to remove book: {str(e)}") from e

    def register_user(self, user):
        """Register an existing user object in the library."""
        try:
            if not user or not user.name:
                logger.warning("Attempt to register invalid user object")
                raise ValueError("User object must have a name")
            
            logger.debug(f"Registering user: '{user.name}'")
            
            query = """
            INSERT INTO users (name, borrow_limit, borrow_days, fine_per_day)
            VALUES (%s, %s, %s, %s)
            RETURNING user_id
            """
            self.cursor.execute(
                query,
                (user.name, user.borrow_limit, user.borrow_days, user.fine_per_day)
            )
            user.user_id = self.cursor.fetchone()[0]
            self.connection.commit()
            
            logger.info(f"User registered successfully: ID={user.user_id}, Name='{user.name}'")
            return f"User '{user.name}' registered"
        except ValueError as e:
            logger.error(f"Validation error while registering user: {str(e)}")
            self.connection.rollback()
            raise
        except Exception as e:
            logger.error(f"Database error while registering user: {str(e)}")
            self.connection.rollback()
            raise DatabaseException(f"Failed to register user: {str(e)}") from e

    def display_books(self):
        """Display all books in the library."""
        try:
            logger.debug("Fetching all books from database")
            
            query = "SELECT book_id, title, author, available FROM books ORDER BY book_id"
            self.cursor.execute(query)
            books = self.cursor.fetchall()

            if not books:
                logger.info("No books found in library")
                return "No books found"

            output = []
            for book in books:
                status = "Available" if book[3] else "Borrowed"
                output.append(
                    f"ID: {book[0]}\n"
                    f"Title: {book[1]}\n"
                    f"Author: {book[2]}\n"
                    f"Status: {status}"
                )

            logger.info(f"Retrieved {len(books)} books from library")
            return "\n\n".join(output)
        except Exception as e:
            logger.error(f"Error displaying books: {str(e)}")
            raise DatabaseException(f"Failed to display books: {str(e)}") from e

    def display_users(self):
        """Display all registered users in the library."""
        try:
            logger.debug("Fetching all users from database")
            
            query = """
            SELECT user_id, name, borrow_limit, borrow_days, fine_per_day
            FROM users
            ORDER BY user_id
            """
            self.cursor.execute(query)
            users = self.cursor.fetchall()

            if not users:
                logger.info("No users registered in library")
                return "No registered users."

            output = []
            for user_row in users:
                user = User(
                    user_row[0],
                    user_row[1],
                    borrow_limit=user_row[2],
                    borrow_days=user_row[3],
                    fine_per_day=float(user_row[4])
                )
                user.borrowed_books = self._get_active_borrowed_books(user.user_id)
                output.append(user.display_details())
            
            logger.info(f"Retrieved {len(users)} users from library")
            return "\n\n".join(output)
        except Exception as e:
            logger.error(f"Error displaying users: {str(e)}")
            raise DatabaseException(f"Failed to display users: {str(e)}") from e

    def lend_book(self, book_id, user_id):
        """Lend a book to a user."""
        try:
            if not book_id or not isinstance(book_id, int):
                raise ValueError("Book ID must be a valid integer")
            if not user_id or not isinstance(user_id, int):
                raise ValueError("User ID must be a valid integer")
            
            logger.debug(f"Processing book lending: Book ID={book_id}, User ID={user_id}")
            
            book = self._find_book(book_id)
            if book is None:
                logger.warning(f"Book not found for lending: ID={book_id}")
                raise BookNotFoundException(f"Book with ID {book_id} not found")
            
            if not book.available:
                logger.warning(f"Book not available for lending: ID={book_id}, Title='{book.title}'")
                raise BookNotAvailableException(f"'{book.title}' is not available right now")

            user = self._find_user(user_id)
            if user is None:
                logger.warning(f"User not found for book lending: ID={user_id}")
                raise UserNotFoundException(f"User with ID {user_id} not found")

            active_count = self._get_active_borrow_count(user_id)
            if active_count >= user.borrow_limit:
                logger.warning(f"User exceeded borrow limit: User ID={user_id}, Count={active_count}, Limit={user.borrow_limit}")
                raise BorrowLimitExceededException(f"Borrow limit reached ({user.borrow_limit} books)")

            self.cursor.execute(
                """
                INSERT INTO borrow_history (user_id, book_id, borrowed_on, due_on, returned_on, fine)
                VALUES (%s, %s, CURRENT_DATE, CURRENT_DATE + %s, NULL, 0.00)
                """,
                (user_id, book_id, user.borrow_days)
            )
            self.cursor.execute(
                "UPDATE books SET available = FALSE WHERE book_id = %s",
                (book_id,)
            )
            self.connection.commit()

            due_date = self._get_due_date(user_id, book_id)
            logger.info(f"Book lent successfully: User='{user.name}', Book='{book.title}', Due Date={due_date}")
            return f"{user.name} borrowed {book.title}. Due on {due_date}."
        except (ValueError, BookNotFoundException, BookNotAvailableException, UserNotFoundException, BorrowLimitExceededException) as e:
            logger.error(f"Error during book lending: {str(e)}")
            self.connection.rollback()
            raise
        except Exception as e:
            logger.error(f"Database error during book lending: {str(e)}")
            self.connection.rollback()
            raise InvalidBorrowException(f"Could not lend book: {str(e)}") from e

    def accept_return(self, book_id, user_id):
        """Process the return of a borrowed book."""
        try:
            if not book_id or not isinstance(book_id, int):
                raise ValueError("Book ID must be a valid integer")
            if not user_id or not isinstance(user_id, int):
                raise ValueError("User ID must be a valid integer")
            
            logger.debug(f"Processing book return: Book ID={book_id}, User ID={user_id}")
            
            book = self._find_book(book_id)
            if book is None:
                logger.warning(f"Book not found for return: ID={book_id}")
                raise BookNotFoundException(f"Book with ID {book_id} not found")

            user = self._find_user(user_id)
            if user is None:
                logger.warning(f"User not found for book return: ID={user_id}")
                raise UserNotFoundException(f"User with ID {user_id} not found")

            self.cursor.execute(
                """
                SELECT history_id, due_on
                FROM borrow_history
                WHERE user_id = %s AND book_id = %s AND returned_on IS NULL
                ORDER BY borrowed_on DESC
                LIMIT 1
                """,
                (user_id, book_id)
            )
            borrow_row = self.cursor.fetchone()
            if borrow_row is None:
                logger.warning(f"No active borrow record: User ID={user_id}, Book ID={book_id}")
                raise InvalidReturnException(f"{user.name} has not borrowed {book.title}")

            history_id, due_on = borrow_row

            self.cursor.execute(
                "SELECT fine_per_day FROM users WHERE user_id = %s",
                (user_id,)
            )
            fine_per_day_row = self.cursor.fetchone()
            fine_per_day = float(fine_per_day_row[0]) if fine_per_day_row else 2.0

            self.cursor.execute("SELECT CURRENT_DATE")
            today = self.cursor.fetchone()[0]
            late_days = max((today - due_on).days, 0)
            fine = late_days * fine_per_day

            self.cursor.execute(
                """
                UPDATE borrow_history
                SET returned_on = CURRENT_DATE, fine = %s
                WHERE history_id = %s
                """,
                (fine, history_id)
            )
            self.cursor.execute(
                "UPDATE books SET available = TRUE WHERE book_id = %s",
                (book_id,)
            )
            self.connection.commit()

            if fine > 0:
                logger.info(f"Book returned with fine: User='{user.name}', Book='{book.title}', Late Days={late_days}, Fine={fine:.2f}")
                return f"{user.name} returned {book.title}. Late by {late_days} days. Fine: {fine:.2f}."
            
            logger.info(f"Book returned on time: User='{user.name}', Book='{book.title}'")
            return f"{user.name} returned {book.title}. No fine."
        except (ValueError, BookNotFoundException, UserNotFoundException, InvalidReturnException) as e:
            logger.error(f"Error during book return: {str(e)}")
            self.connection.rollback()
            raise
        except Exception as e:
            logger.error(f"Database error during book return: {str(e)}")
            self.connection.rollback()
            raise InvalidReturnException(f"Could not return book: {str(e)}") from e

    def display_available_books(self):
        """Display all available books in the library."""
        try:
            logger.debug("Fetching available books from database")
            
            query = """
            SELECT book_id, title, author, available
            FROM books
            WHERE available = TRUE
            ORDER BY book_id
            """
            self.cursor.execute(query)
            books = self.cursor.fetchall()

            if not books:
                logger.info("No available books found in library")
                return "No available books."

            output = []
            for book in books:
                output.append(Book(book[0], book[1], book[2], book[3]).display_details())
            
            logger.info(f"Retrieved {len(books)} available books from library")
            return "\n\n".join(output)
        except Exception as e:
            logger.error(f"Error displaying available books: {str(e)}")
            raise DatabaseException(f"Failed to display available books: {str(e)}") from e

    def search_books(self, query_text):
        """Search for books by title or author."""
        try:
            if not query_text or not query_text.strip():
                logger.warning("Search attempted with empty query")
                raise ValueError("Search query cannot be empty")
            
            logger.debug(f"Searching books with query: '{query_text}'")
            
            query = """
            SELECT book_id, title, author
            FROM books
            WHERE title ILIKE %s OR author ILIKE %s
            ORDER BY book_id
            """

            search_pattern = f"%{query_text}%"
            self.cursor.execute(query, (search_pattern, search_pattern))

            books = self.cursor.fetchall()

            if not books:
                logger.info(f"No books found matching search: '{query_text}'")
                return "No books found"

            output = []
            for book in books:
                output.append(f"{book[1]} by {book[2]}")

            logger.info(f"Search found {len(books)} books matching: '{query_text}'")
            return "\n".join(output)
        except ValueError as e:
            logger.error(f"Validation error in search: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error searching books: {str(e)}")
            raise DatabaseException(f"Failed to search books: {str(e)}") from e

    def display_user_borrow_history(self, user_id):
        """Display borrow history for a specific user."""
        try:
            if not user_id or not isinstance(user_id, int):
                raise ValueError("User ID must be a valid integer")
            
            logger.debug(f"Fetching borrow history for User ID: {user_id}")
            
            user = self._find_user(user_id)
            if user is None:
                logger.warning(f"User not found for history retrieval: ID={user_id}")
                raise UserNotFoundException(f"User with ID {user_id} not found")

            self.cursor.execute(
                """
                SELECT bh.book_id, b.title, bh.borrowed_on, bh.due_on, bh.returned_on, bh.fine
                FROM borrow_history bh
                JOIN books b ON b.book_id = bh.book_id
                WHERE bh.user_id = %s
                ORDER BY bh.borrowed_on DESC
                """,
                (user_id,)
            )
            history_rows = self.cursor.fetchall()

            if not history_rows:
                logger.info(f"No borrow history found for User ID: {user_id}")
                return f"No borrow history for {user.name}."

            lines = []
            for row in history_rows:
                returned_on = row[4] if row[4] is not None else "Not returned"
                lines.append(
                    f"Book ID: {row[0]} | Title: {row[1]} | "
                    f"Borrowed: {row[2]} | Due: {row[3]} | "
                    f"Returned: {returned_on} | Fine: {float(row[5]):.2f}"
                )

            logger.info(f"Retrieved {len(history_rows)} borrow history records for User: '{user.name}'")
            return "\n".join(lines)
        except (ValueError, UserNotFoundException) as e:
            logger.error(f"Error retrieving borrow history: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Database error retrieving borrow history: {str(e)}")
            raise DatabaseException(f"Failed to display borrow history: {str(e)}") from e

    def _find_book(self, book_id):
        """Find a book by ID."""
        try:
            logger.debug(f"Finding book with ID: {book_id}")
            self.cursor.execute(
                "SELECT book_id, title, author, available FROM books WHERE book_id = %s",
                (book_id,)
            )
            book_row = self.cursor.fetchone()
            if book_row is None:
                logger.debug(f"Book not found: ID={book_id}")
                return None
            logger.debug(f"Book found: ID={book_id}, Title='{book_row[1]}'")
            return Book(book_row[0], book_row[1], book_row[2], book_row[3])
        except Exception as e:
            logger.error(f"Error finding book: {str(e)}")
            raise

    def _find_user(self, user_id):
        """Find a user by ID."""
        try:
            logger.debug(f"Finding user with ID: {user_id}")
            self.cursor.execute(
                """
                SELECT user_id, name, borrow_limit, borrow_days, fine_per_day
                FROM users
                WHERE user_id = %s
                """,
                (user_id,)
            )
            user_row = self.cursor.fetchone()
            if user_row is None:
                logger.debug(f"User not found: ID={user_id}")
                return None

            user = User(
                user_row[0],
                user_row[1],
                borrow_limit=user_row[2],
                borrow_days=user_row[3],
                fine_per_day=float(user_row[4])
            )
            user.borrowed_books = self._get_active_borrowed_books(user_id)
            logger.debug(f"User found: ID={user_id}, Name='{user_row[1]}'")
            return user
        except Exception as e:
            logger.error(f"Error finding user: {str(e)}")
            raise

    def _get_active_borrow_count(self, user_id):
        """Get the count of active borrowed books for a user."""
        try:
            logger.debug(f"Getting active borrow count for User ID: {user_id}")
            self.cursor.execute(
                """
                SELECT COUNT(*)
                FROM borrow_history
                WHERE user_id = %s AND returned_on IS NULL
                """,
                (user_id,)
            )
            count = self.cursor.fetchone()[0]
            logger.debug(f"Active borrow count for User ID {user_id}: {count}")
            return count
        except Exception as e:
            logger.error(f"Error getting active borrow count: {str(e)}")
            raise

    def _get_active_borrowed_books(self, user_id):
        """Get list of actively borrowed books for a user."""
        try:
            logger.debug(f"Getting active borrowed books for User ID: {user_id}")
            self.cursor.execute(
                """
                SELECT b.book_id, b.title, b.author, b.available
                FROM borrow_history bh
                JOIN books b ON b.book_id = bh.book_id
                WHERE bh.user_id = %s AND bh.returned_on IS NULL
                ORDER BY bh.borrowed_on DESC
                """,
                (user_id,)
            )
            books = [Book(row[0], row[1], row[2], row[3]) for row in self.cursor.fetchall()]
            logger.debug(f"Found {len(books)} active borrowed books for User ID: {user_id}")
            return books
        except Exception as e:
            logger.error(f"Error getting active borrowed books: {str(e)}")
            raise

    def _get_due_date(self, user_id, book_id):
        """Get the due date for a borrowed book."""
        try:
            logger.debug(f"Getting due date for User ID: {user_id}, Book ID: {book_id}")
            self.cursor.execute(
                """
                SELECT due_on
                FROM borrow_history
                WHERE user_id = %s AND book_id = %s AND returned_on IS NULL
                ORDER BY borrowed_on DESC
                LIMIT 1
                """,
                (user_id, book_id)
            )
            due_row = self.cursor.fetchone()
            due_date = due_row[0] if due_row else "Unknown"
            logger.debug(f"Due date retrieved: {due_date}")
            return due_date
        except Exception as e:
            logger.error(f"Error getting due date: {str(e)}")
            raise
