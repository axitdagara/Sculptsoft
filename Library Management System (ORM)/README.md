# Library Management System

Console-based Library Management System built with Python and PostgreSQL.

## Overview
This project helps you manage a small library from the terminal. You can:
- Add and remove books
- Register users
- Lend and return books
- View available books
- Search books by title or author
- Track borrow history per user
- Apply automatic late-return fines

## Tech Stack
- Python 3.9+
- PostgreSQL
- `psycopg2`
- `python-dotenv`

## Project Structure
```text
.
|-- main.py
|-- README.md
|-- config/
|   |-- __init__.py
|   |-- db.py
|   `-- exceptions.py
|-- database/
|   `-- schema.sql
|-- models/
|   |-- __init__.py
|   |-- book.py
|   `-- user.py
`-- services/
    |-- __init__.py
    `-- library.py
```

## Setup

### 1. Create and activate virtual environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies
```powershell
pip install psycopg2-binary python-dotenv
```

### 3. Configure environment variables
Create or update `.env` in the project root with:

```env
host=localhost
user=your_postgres_user
password=your_postgres_password
database=your_database_name
port=5432
```

### 4. Ensure PostgreSQL database exists
Create the database referenced by `database` in `.env`.

Note: The application also auto-creates required tables at startup if they do not exist.

## Run the Application
```powershell
python main.py
```

## Menu Options
When the app starts, you can use:
1. Add book
2. Register user
3. Lend book
4. Return book
5. Show all books
6. Show registered users
7. Show available books
8. Remove book
9. Search books by title/author
10. Show user borrow history
11. Exit

## Default Library Rules
- Borrow limit per user: `3` books
- Borrow period: `14` days
- Fine per late day: `2.00`

## Database Tables
- `books`
- `users`
- `borrow_history`

The schema file is available at `database/schema.sql`, and table creation is also handled in `services/library.py`.

## Error Handling
The app uses custom exceptions in `config/exceptions.py` for common failure cases, including:
- Database connection issues
- Missing users or books
- Borrow limit violations
- Invalid borrow/return operations

## Future Improvements
- Add unit tests
- Add CLI argument support
- Add logging configuration file
- Add Docker support for PostgreSQL + app
