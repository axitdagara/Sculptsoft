create database Facebook ;
use Facebook ;
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(10),
    date_of_birth DATE,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_online BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
select * from users ;

CREATE TABLE user_interests (
    interest_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    interest_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
select * from user_interests ; 

CREATE TABLE posts (
    post_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    group_id INT NULL,
    post_content TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
select * from posts ;
alter table posts drop group_id ; 

CREATE TABLE comments (
    comment_id INT PRIMARY KEY AUTO_INCREMENT,
    post_id INT NOT NULL,
    user_id INT NOT NULL,
    parent_comment_id INT NULL,
    comment_text TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(post_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (parent_comment_id) REFERENCES comments(comment_id)
);
select * from comments ;

CREATE TABLE reactions (
    reaction_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    post_id INT NULL,
    comment_id INT NULL,
    reaction_type ENUM('LIKE', 'DISLIKE') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id),
    FOREIGN KEY (comment_id) REFERENCES comments(comment_id),
    CHECK (
        (post_id IS NOT NULL AND comment_id IS NULL)
        OR
        (post_id IS NULL AND comment_id IS NOT NULL)
    )
);
select * from reactions ;

CREATE TABLE groupss (
    group_id INT PRIMARY KEY AUTO_INCREMENT,
    group_name VARCHAR(100) NOT NULL,
    group_description TEXT,
    admin_user_id INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_user_id)REFERENCES users(user_id)
);
select * from groupss ;
drop table groupss ;
drop table `groups`;
SHOW DATABASES;
show tables ;


CREATE TABLE group_members (
    group_member_id INT PRIMARY KEY AUTO_INCREMENT,
    group_id INT NOT NULL,
    user_id INT NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id)REFERENCES groupss(group_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    UNIQUE(group_id, user_id)
);
select * from group_members ;

CREATE TABLE friend_requests (
    request_id INT PRIMARY KEY AUTO_INCREMENT,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    request_status ENUM( 'PENDING','ACCEPTED','REJECTED') DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(user_id),
    FOREIGN KEY (receiver_id)REFERENCES users(user_id)
);
select * from friend_requests ;

CREATE TABLE friends (
    friendship_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    friend_user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (friend_user_id) REFERENCES users(user_id),
    UNIQUE(user_id, friend_user_id)
);
select * from friends ;


CREATE TABLE post_shares (
    share_id INT PRIMARY KEY AUTO_INCREMENT,
    post_id INT NOT NULL,
    shared_by_user_id INT NOT NULL,
    shared_to_user_id INT NULL,
    shared_to_group_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(post_id),
    FOREIGN KEY (shared_by_user_id) REFERENCES users(user_id),
    FOREIGN KEY (shared_to_user_id) REFERENCES users(user_id),
    FOREIGN KEY (shared_to_group_id) REFERENCES groupss(group_id),
    CHECK (
        (shared_to_user_id IS NOT NULL AND shared_to_group_id IS NULL)
        OR
        (shared_to_user_id IS NULL AND shared_to_group_id IS NOT NULL)
    )
);

show tables ;
describe users ;


-- table 1 
INSERT INTO users 
(first_name, last_name, gender, date_of_birth, email, password_hash, is_online)
VALUES
('Harsh', 'Koradiya', 'Male', '2003-05-12', 'harsh@gmail.com', 'pass123', TRUE),
('Aman', 'Sharma', 'Male', '2001-07-19', 'aman@gmail.com', 'pass234', FALSE),
('Priya', 'Patel', 'Female', '2002-03-25', 'priya@gmail.com', 'pass345', TRUE),
('Rohit', 'Verma', 'Male', '2000-11-10', 'rohit@gmail.com', 'pass456', FALSE),
('Neha', 'Joshi', 'Female', '2001-09-15', 'neha@gmail.com', 'pass567', TRUE);


-- table 2
INSERT INTO user_interests (user_id, interest_name)
VALUES
(1, 'Coding'),
(1, 'AI'),
(2, 'Gaming'),
(3, 'Photography'),
(4, 'Music'),
(5, 'Traveling');


select * from user_interests ;
truncate table user_interests ;


-- table 3 
INSERT INTO posts (user_id, post_content)
VALUES
(1, 'Learning SQL normalization today'),
(2, 'MongoDB is very flexible'),
(3, 'Beautiful sunset today'),
(4, 'React frontend completed'),
(5, 'Working on Flask backend');

select * from posts ;
truncate table posts ;


-- table 4

INSERT INTO comments
(post_id, user_id, parent_comment_id, comment_text)
VALUES
(1, 2, NULL, 'Great post!'),
(1, 3, 1, 'I agree with you'),
(2, 1, NULL, 'Nice information'),
(3, 5, NULL, 'Amazing picture'),
(4, 2, NULL, 'Good work on frontend');

-- table 5 

INSERT INTO reactions
(user_id, post_id, comment_id, reaction_type)
VALUES
(2, 1, NULL, 'LIKE'),
(3, 1, NULL, 'LIKE'),
(4, 2, NULL, 'DISLIKE'),
(1, NULL, 1, 'LIKE'),
(5, NULL, 4, 'LIKE');

-- table 6 
INSERT INTO groupss
(group_name, group_description, admin_user_id)
VALUES
('Python Developers', 'Group for Python learners', 1),
('React Community', 'Frontend developers group', 2),
('Photography Club', 'Share photography ideas', 3),
('Music Lovers', 'Music discussions', 4),
('Travel Buddies', 'Travel experiences and tips', 5);

-- table 7 
INSERT INTO group_members
(group_id, user_id)
VALUES
(1, 1),
(1, 2),
(2, 3),
(3, 4),
(5, 5);


-- table 8
INSERT INTO friend_requests
(sender_id, receiver_id, request_status)
VALUES
(1, 2, 'ACCEPTED'),
(2, 3, 'PENDING'),
(3, 4, 'REJECTED'),
(4, 5, 'ACCEPTED'),
(5, 1, 'PENDING');

-- table 9
INSERT INTO friends
(user_id, friend_user_id)
VALUES
(1, 2),
(1, 3),
(2, 4),
(3, 5),
(4, 5);



-- table 10
INSERT INTO post_shares
(post_id, shared_by_user_id, shared_to_user_id, shared_to_group_id)
VALUES
(1, 1, NULL, 1),
(2, 2, NULL, 2),
(3, 3, 4, NULL),
(4, 4, NULL, 3),
(5, 5, 1, NULL);


SELECT * FROM users;
SELECT * FROM user_interests;
SELECT * FROM posts;
SELECT * FROM comments;
SELECT * FROM reactions;
SELECT * FROM groupss;
SELECT * FROM group_members;
SELECT * FROM friend_requests;
SELECT * FROM friends;
SELECT * FROM post_shares;



