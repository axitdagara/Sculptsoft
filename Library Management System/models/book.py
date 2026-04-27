class Book:
    def __init__(self, book_id , title, author, available=True):
        self.book_id = book_id
        self.author = author
        self.title = title
        self.available = available

    def mark_borrowed(self):
        if self.available:
            self.available = False
            return True
        return False

    def mark_returned(self):
        self.available = True

    def display_details(self):
        status = "Available" if self.available else "Borrowed"
        return (
            f"Book ID : {self.book_id}\n"
            f"Title   : {self.title}\n"
            f"Author  : {self.author}\n"
            f"Status  : {status}"
        )
