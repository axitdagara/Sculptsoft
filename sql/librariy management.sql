CREATE DATABASE library_management_system;

USE library_management_system;



CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    borrow_limit INT DEFAULT 3,
    borrow_days INT DEFAULT 14,
    fine_per_day DECIMAL(10,2) DEFAULT 2.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);




CREATE TABLE books (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE borrow_records (
    borrow_id INT PRIMARY KEY AUTO_INCREMENT,

    user_id INT NOT NULL,
    book_id INT NOT NULL,

    borrowed_on DATE NOT NULL,
    due_on DATE NOT NULL,
    returned_on DATE NULL,

    fine DECIMAL(10,2) DEFAULT 0.00,

    status ENUM('BORROWED', 'RETURNED') DEFAULT 'BORROWED',

    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE,

    FOREIGN KEY (book_id) REFERENCES books(book_id)
        ON DELETE CASCADE
);