from config.db import create_connection
from models.book import Book
from models.user import User


class Library:
    def __init__(self):
        self.connection = create_connection()
        if self.connection is None:
            raise RuntimeError("Database connection could not be established.")

        self.cursor = self.connection.cursor()
        self._ensure_tables()

    def _ensure_tables(self):
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
        self.connection.commit()

    def create_book(self, title, author):
        try:
            query = """
            INSERT INTO books (title, author, available)
            VALUES (%s, %s, %s)
            RETURNING book_id
            """
            self.cursor.execute(query, (title, author, True))
            book_id = self.cursor.fetchone()[0]
            self.connection.commit()
            return Book(book_id, title, author, True)
        except Exception as e:
            self.connection.rollback()
            return str(e)

    def create_user(self, name):
        try:
            query = """
            INSERT INTO users (name, borrow_limit, borrow_days, fine_per_day)
            VALUES (%s, %s, %s, %s)
            RETURNING user_id
            """
            self.cursor.execute(query, (name, 3, 14, 2.0))
            user_id = self.cursor.fetchone()[0]
            self.connection.commit()
            return User(user_id, name)
        except Exception as e:
            self.connection.rollback()
            return str(e)

    def add_book(self, book):
        try:
            query = """
            INSERT INTO books (title, author, available)
            VALUES (%s, %s, %s)
            RETURNING book_id
            """
            self.cursor.execute(query, (book.title, book.author, book.available))
            book.book_id = self.cursor.fetchone()[0]
            self.connection.commit()
            return f"Book '{book.title}' added successfully"
        except Exception as e:
            self.connection.rollback()
            return str(e)

    def remove_book(self, book_id):
        try:
            query = "DELETE FROM books WHERE book_id = %s"
            self.cursor.execute(query, (book_id,))
            self.connection.commit()

            if self.cursor.rowcount == 0:
                return "Book not found."
            return "Book removed successfully"

        except Exception as e:
            self.connection.rollback()
            return str(e)

    def register_user(self, user):
        try:
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
            return f"User '{user.name}' registered"

        except Exception as e:
            self.connection.rollback()
            return str(e)

    def display_books(self):
        try:
            query = "SELECT book_id, title, author, available FROM books ORDER BY book_id"
            self.cursor.execute(query)
            books = self.cursor.fetchall()

            if not books:
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

            return "\n\n".join(output)

        except Exception as e:
            return str(e)

    def display_users(self):
        try:
            query = """
            SELECT user_id, name, borrow_limit, borrow_days, fine_per_day
            FROM users
            ORDER BY user_id
            """
            self.cursor.execute(query)
            users = self.cursor.fetchall()

            if not users:
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
            return "\n\n".join(output)
        except Exception as e:
            return str(e)

    def lend_book(self, book_id, user_id):
        try:
            book = self._find_book(book_id)
            if book is None:
                return "Book not found."
            if not book.available:
                return f"{book.title} is not available right now."



            user = self._find_user(user_id)
            if user is None:
                return "User not found."

            active_count = self._get_active_borrow_count(user_id)
            if active_count >= user.borrow_limit:
                return f"Borrow limit reached ({user.borrow_limit} books)."

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
            return f"{user.name} borrowed {book.title}. Due on {due_date}."
        except Exception:
            self.connection.rollback()
            return "Could not lend book."

    def accept_return(self, book_id, user_id):
        try:
            book = self._find_book(book_id)
            if book is None:
                return "Book not found."

            user = self._find_user(user_id)
            if user is None:
                return "User not found."

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
                return f"{user.name} has not borrowed {book.title}."

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
                return f"{user.name} returned {book.title}. Late by {late_days} days. Fine: {fine:.2f}."
            return f"{user.name} returned {book.title}. No fine."
        except Exception:
            self.connection.rollback()
            return "Could not return book."

    def display_available_books(self):
        try:
            query = """
            SELECT book_id, title, author, available
            FROM books
            WHERE available = TRUE
            ORDER BY book_id
            """
            self.cursor.execute(query)
            books = self.cursor.fetchall()

            if not books:
                return "No available books."

            output = []
            for book in books:
                output.append(Book(book[0], book[1], book[2], book[3]).display_details())
            return "\n\n".join(output)
        except Exception as e:
            return str(e)

    def search_books(self, query_text):
        try:
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
                return "No books found"

            output = []

            for book in books:
                output.append(f"{book[1]} by {book[2]}")

            return "\n".join(output)

        except Exception as e:
            return str(e)

    def display_user_borrow_history(self, user_id):
        try:
            user = self._find_user(user_id)
            if user is None:
                return "User not found."

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
                return f"No borrow history for {user.name}."

            lines = []
            for row in history_rows:
                returned_on = row[4] if row[4] is not None else "Not returned"
                lines.append(
                    f"Book ID: {row[0]} | Title: {row[1]} | "
                    f"Borrowed: {row[2]} | Due: {row[3]} | "
                    f"Returned: {returned_on} | Fine: {float(row[5]):.2f}"
                )

            return "\n".join(lines)
        except Exception as e:
            return str(e)

    def _find_book(self, book_id):
        self.cursor.execute(
            "SELECT book_id, title, author, available FROM books WHERE book_id = %s",
            (book_id,)
        )
        book_row = self.cursor.fetchone()
        if book_row is None:
            return None
        return Book(book_row[0], book_row[1], book_row[2], book_row[3])

    def _find_user(self, user_id):
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
            return None

        user = User(
            user_row[0],
            user_row[1],
            borrow_limit=user_row[2],
            borrow_days=user_row[3],
            fine_per_day=float(user_row[4])
        )
        user.borrowed_books = self._get_active_borrowed_books(user_id)
        return user

    def _get_active_borrow_count(self, user_id):
        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM borrow_history
            WHERE user_id = %s AND returned_on IS NULL
            """,
            (user_id,)
        )
        return self.cursor.fetchone()[0]

    def _get_active_borrowed_books(self, user_id):
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
        return [Book(row[0], row[1], row[2], row[3]) for row in self.cursor.fetchall()]

    def _get_due_date(self, user_id, book_id):
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
        return due_row[0] if due_row else "Unknown"
