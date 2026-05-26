DROP TABLE IF EXISTS borrow_history CASCADE;
DROP TABLE IF EXISTS books CASCADE;
DROP TABLE IF EXISTS users CASCADE;



CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,

    name VARCHAR(150) NOT NULL,

    borrow_limit INT DEFAULT 3,

    borrow_days INT DEFAULT 14,

    fine_per_day DECIMAL(10,2) DEFAULT 0.00,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,

    title VARCHAR(255) NOT NULL,

    author VARCHAR(255) NOT NULL,

    available BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);




CREATE TABLE borrow_history (

    history_id SERIAL PRIMARY KEY,

    user_id INT NOT NULL,

    book_id INT NOT NULL,

    borrowed_on DATE NOT NULL DEFAULT CURRENT_DATE,

    due_on DATE NOT NULL,

    returned_on DATE,

    fine DECIMAL(10,2) DEFAULT 0.00,

    status VARCHAR(20) DEFAULT 'BORROWED',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_history_user
        FOREIGN KEY(user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_history_book
        FOREIGN KEY(book_id)
        REFERENCES books(book_id)
        ON DELETE CASCADE
);




CREATE INDEX idx_books_title
ON books(title);

CREATE INDEX idx_books_author
ON books(author);

CREATE INDEX idx_history_user
ON borrow_history(user_id);

CREATE INDEX idx_history_book
ON borrow_history(book_id);

CREATE INDEX idx_history_status
ON borrow_history(status);



SELECT * FROM books;

SELECT * FROM users;
truncate table users ; 

SELECT * FROM borrow_history;