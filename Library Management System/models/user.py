from datetime import date, timedelta


class User:

    def __init__(self, user_id , name, borrow_limit=3, borrow_days=14, fine_per_day=2.0):
        self.user_id = user_id
        self.name = name
        self.borrowed_books = []
        self.borrow_limit = borrow_limit
        self.borrow_days = borrow_days
        self.fine_per_day = fine_per_day
        self.borrowed_on = {}
        self.due_on = {}
        self.borrow_history = []

    def get_role(self):
        return "User"

    def display_details(self):
        borrowed_titles = " , ".join(book.title for book in self.borrowed_books) or "None"
        return (
            f"User ID        : {self.user_id}\n"
            f"Name           : {self.name}\n"
            f"Role           : {self.get_role()}\n"
            f"Borrow Limit   : {self.borrow_limit}\n"
            f"Borrowed Books : {borrowed_titles}"
        )

    def display_borrow_history(self):
        if not self.borrow_history:
            return f"No borrow history for {self.name}."

        lines = []
        for entry in self.borrow_history:
            fine_text = f"{entry['fine']:.2f}"
            lines.append(
                f"Book ID: {entry['book_id']} | Title: {entry['title']} | "
                f"Borrowed: {entry['borrowed_on']} | Due: {entry['due_on']} | "
                f"Returned: {entry['returned_on']} | Fine: {fine_text}"
            )

        return "\n".join(lines)

    def borrow_book(self, book):                               ## gpt
        try:
            if len(self.borrowed_books) >= self.borrow_limit:
                return f"Borrow limit reached ({self.borrow_limit} books)."

            if not book.mark_borrowed():
                return f"{book.title} is not available right now."

            self.borrowed_books.append(book)
            borrowed_date = date.today()
            due_date = borrowed_date + timedelta(days=self.borrow_days)
            self.borrowed_on[book.book_id] = borrowed_date
            self.due_on[book.book_id] = due_date
            self.borrow_history.append(
                {
                    "book_id": book.book_id,
                    "title": book.title,
                    "borrowed_on": str(borrowed_date),
                    "due_on": str(due_date),
                    "returned_on": "Not returned",
                    "fine": 0.0,
                }
            )
            return f"{self.name} borrowed {book.title}. Due on {due_date}."
        except Exception:
            return "Could not borrow book."

    def return_book(self, book):
        try:
            if book not in self.borrowed_books:
                return f"{self.name} has not borrowed {book.title}"

            book.mark_returned()

            self.borrowed_books.remove(book)                     ##gpt
            today = date.today()
            due_date = self.due_on.pop(book.book_id, today)
            self.borrowed_on.pop(book.book_id, None)
            late_days = max((today - due_date).days, 0)
            fine = late_days * self.fine_per_day

            for entry in reversed(self.borrow_history):
                if entry["book_id"] == book.book_id and entry["returned_on"] == "Not returned":
                    entry["returned_on"] = str(today)
                    entry["fine"] = fine                                ### gpt
                    break

            if fine > 0:
                return f"{self.name} returned {book.title}. Late by {late_days} days. Fine: {fine:.2f}."
            return f"{self.name} returned {book.title}. No fine."
        except Exception:
            return "Could not return book."
