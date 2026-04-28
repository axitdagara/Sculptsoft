create database employee ;
use employee ;
create table if not exists emp_infoo ( 
				id int primary key ,
                e_name varchar (50) , 
                salary int , domain varchar (50) );

insert into emp_infoo value (1 , "axit" , 5000 , "python") ;
insert into emp_infoo values  (2 , "harsh" , 4500 , "python") , 
                              (3 , "jaydeep" , 7000 , "AIML") ,
                              (4 , "pratham" , 5000 , "AIML") ; 
select * from emp_infoo; 
select * from emp_infoo where salary > 5000 ;
select e_name , domain from emp_infoo where salary > 5000 ;




