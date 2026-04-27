
from models.book import Book
from models.user import User


class Library:
    def __init__(self):
        self.collection_of_books = []
        self.list_of_users = []
        self._next_book_id = 1
        self._next_user_id = 1

    def _generate_book_id(self):
        while self._find_book(self._next_book_id) is not None:
            self._next_book_id += 1
        generated_id = self._next_book_id
        self._next_book_id += 1
        return generated_id

    def _generate_user_id(self):
        while self._find_user(self._next_user_id) is not None:
            self._next_user_id += 1
        generated_id = self._next_user_id
        self._next_user_id += 1
        return generated_id

    def create_book(self, title, author):
        book = Book(self._generate_book_id(), title, author)
        self.add_book(book)
        return book

    def create_user(self, name):
        user = User(self._generate_user_id(), name)
        self.register_user(user)
        return user

    def add_book(self, book):
        try:
            if self._find_book(book.book_id) is not None:
                return f"Book ID '{book.book_id}' already exists."

            self.collection_of_books.append(book)
            if isinstance(book.book_id, int) and book.book_id >= self._next_book_id:
                self._next_book_id = book.book_id + 1
            return f"Book '{book.title}' added."
        except Exception:
            return "Could not add book."

    def remove_book(self, book_id):
        for book in self.collection_of_books:
            if book.book_id == book_id:
                self.collection_of_books.remove(book)
                return f"Book '{book.title}' removed."
        return "Book not found."

    def register_user(self, user):
        try:
            if self._find_user(user.user_id) is not None:
                return f"User ID '{user.user_id}' already exists."

            self.list_of_users.append(user)
            if isinstance(user.user_id, int) and user.user_id >= self._next_user_id:
                self._next_user_id = user.user_id + 1
            return f"User '{user.name}' registered."
        except Exception:
            return "Could not register user."

    def display_books(self):
        if len(self.collection_of_books) == 0:
            return "No books in the library."

        output = []
        for book in self.collection_of_books:
            output.append(book.display_details())
        return "\n\n".join(output)

    def display_users(self):
        if len(self.list_of_users) == 0:
            return "No registered users."

        output = []
        for user in self.list_of_users:
            output.append(user.display_details())
        return "\n\n".join(output)

    def lend_book(self, book_id, user_id):
        try:
            book = self._find_book(book_id)
            if book is None:
                return "Book not found."

            user = self._find_user(user_id)
            if user is None:
                return "User not found."

            return user.borrow_book(book)
        except Exception:
            return "Could not lend book."

    def accept_return(self, book_id, user_id):
        try:
            book = self._find_book(book_id)
            if book is None:
                return "Book not found."

            user = self._find_user(user_id)
            if user is None:
                return "User not found."

            return user.return_book(book)
        except Exception:
            return "Could not return book."

    def display_available_books(self):
        available_books = []
        for book in self.collection_of_books:
            if book.available:
                available_books.append(book)

        if len(available_books) == 0:
            return "No available books."

        output = []
        for book in available_books:
            output.append(book.display_details())
        return "\n\n".join(output)

    def search_books(self, query):
        try:
            text = query.strip().lower()
            if text == "":
                return "Please enter a search term."

            matches = []
            for book in self.collection_of_books:
                if text in book.title.lower() or text in book.author.lower():
                    matches.append(book)

            if len(matches) == 0:
                return "No books match your search."

            output = []
            for book in matches:
                output.append(book.display_details())
            return "\n\n".join(output)
        except Exception:
            return "Search failed."

    def display_user_borrow_history(self, user_id):
        user = self._find_user(user_id)
        if user is None:
            return "User not found."
        return user.display_borrow_history()

    def _find_book(self, book_id):
        for book in self.collection_of_books:
            if book.book_id == book_id:
                return book
        return None

    def _find_user(self, user_id):
        for user in self.list_of_users:
            if user.user_id == user_id:
                return user
        return None
