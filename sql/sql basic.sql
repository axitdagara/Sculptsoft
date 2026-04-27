create database students ;
use students ;
create table student (id int primary key , name varchar (50) , age int not null);
show  databases ;
show tables ;

select * from student ;


insert into  student (id , name ,  age)  values (101 , "axit" , 24) ,(102 , "yash" , 24) , (103 , "hari" , 22) ;
show tables ;
select * from student ;

create table stud_info (stud_id int , foreign key(stud_id) references student(id) )









