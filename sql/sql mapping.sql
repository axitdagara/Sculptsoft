create database student_recordss ;
use student_recordss ; 
CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    age INT,
    city VARCHAR(100)
);

CREATE TABLE courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(100),
    duration VARCHAR(50)
);


CREATE TABLE student_courses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    course_id INT,

    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);



INSERT INTO students (name, age, city)
VALUES
('Harsh', 21, 'Ahmedabad'),
('Rahul', 22, 'Surat'),
('Priya', 20, 'Rajkot');


INSERT INTO courses (course_name, duration)
VALUES
('Python', '3 Months'),
('SQL', '2 Months'),
('Web Development', '4 Months');


INSERT INTO student_courses (student_id, course_id)
VALUES
(1, 1),
(1, 2),
(2, 2),
(3, 3);



SELECT students.name, courses.course_name FROM student_courses JOIN students ON student_courses.student_id = students.student_id
                                  JOIN courses ON student_courses.course_id = courses.course_id;