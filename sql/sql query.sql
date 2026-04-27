create database college ;
use college ;
create table student(rollno int primary key , name varchar (50) , marks int not null , grade varchar (2) , city varchar(20));
insert into student (rollno , name , marks , grade , city ) values (101 , "axit" , 90 , "A" , "ahmedabad") , (102 , "yash" , 93 , "A" , "surat") , (103 , "hari" , 85 , "B" , "sanand"), (104 , "jay" , 78 , "C" , "ahmedabad") , (105 , "harsh" , 50 , "D" , "ahmedabad");


select name , grade from student;
select name , grade from student where marks > 90 ;
select * from student where marks > 80 and city = "ahmedabad" ;
select * from student where marks > 80 or city = "ahmedabad" ;
select * from student where marks between 80 and 90 ;
select * from student where grade in ("A" , "B" ) ;
select * from student where grade NOT in ("A" , "B" ) ;
select * from student limit 3 ;
select name , grade , marks from student limit 3 ;
select * from student order by  marks ASC ;
select * from student order by  marks desc ;
select max(marks) from student ;
select min(marks) from student ;
select avg(marks) from student ;
select sum(marks) from student ;
select count(marks) from student ;
select city , count(name) from student group by city ;
select city , count(name) from student group by city having max(marks) > 90 ;
select city , count(name) from student group by city having max(marks) between 80 and 95 ;
select city , count(name) from student group by city having max(marks) between 80 and 95 order by city ASC ;


SET SQL_SAFE_UPDATES = 0 ;
update student set grade = "O" where grade = "A" ;
select grade from student ;

delete from student where marks < 33 ;

alter table student add column id int unique ;
alter table student drop column id ;
alter table student rename to studentinfo ;
alter table student change column id  stud_id  int unique ;
alter table student modify stud_id int  ;
alter table student modify stud_id int unique  ;
truncate table student ;



