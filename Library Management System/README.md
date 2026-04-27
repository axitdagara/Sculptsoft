# Library Management System

Simple console-based Library Management System built with Python.

## Features
- Add and remove books
- Register users
- Lend and return books
- Search books by title or author
- Borrow limit per user
- Borrow history
- Basic fine logic on late returns
- Simple try/except error handling

## Project Structure
- main.py
- models/
  - book.py
  - user.py
- services/
  - library.py

## How to Run
1. Open terminal in project folder.
2. Run:

```bash
python main.py
```

## Notes
- Default borrow limit: 3 books per user
- Default borrow period: 14 days
- Default fine: 2.0 per late day
