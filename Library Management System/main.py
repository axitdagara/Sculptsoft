
from services.library import Library


def print_section(title, content):
    separator = "=" * len(title)
    print(f"\n{separator}\n{title}\n{separator}")
    print(content)


def read_int(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Please enter a valid number.")


def print_menu():
    print("\nLibrary Management System")
    print("1. Add book")
    print("2. Register user")
    print("3. Lend book")
    print("4. Return book")
    print("5. Show all books")
    print("6. Show registered users")
    print("7. Show available books")
    print("8. Remove book")
    print("9. Search books by title/author")
    print("10. Show user borrow history")
    print("11. Exit")


def main():
    library = Library()

    while True:
        try:
            print_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                title = input("Enter title: ").strip()
                author = input("Enter author: ").strip()
                new_book = library.create_book(title, author)
                print(f"Book '{new_book.title}' added with ID {new_book.book_id}.")
            elif choice == "2":
                name = input("Enter name: ").strip()
                new_user = library.create_user(name)
                print(f"User '{new_user.name}' registered with ID {new_user.user_id}.")
            elif choice == "3":
                book_id = read_int("Enter book ID to lend: ")
                user_id = read_int("Enter user ID: ")
                print(library.lend_book(book_id, user_id))
            elif choice == "4":
                book_id = read_int("Enter book ID to return: ")
                user_id = read_int("Enter user ID: ")
                print(library.accept_return(book_id, user_id))
            elif choice == "5":
                print_section("Library Catalog", library.display_books())
            elif choice == "6":
                print_section("Registered Users", library.display_users())
            elif choice == "7":
                print_section("Available Books", library.display_available_books())
            elif choice == "8":
                book_id = read_int("Enter book ID to remove: ")
                print(library.remove_book(book_id))
            elif choice == "9":
                query = input("Enter title/author keyword: ").strip()
                print_section("Search Results", library.search_books(query))
            elif choice == "10":
                user_id = read_int("Enter user ID: ")
                print_section("Borrow History", library.display_user_borrow_history(user_id))
            elif choice == "11":
                print("Exiting library system.")
                break
            else:
                print("Invalid choice. Please select a valid option.")
        except Exception:
            print("Something went wrong. Please try again.")


if __name__ == "__main__":
    main()