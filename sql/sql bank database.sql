create database bank ;
use bank ;
create table account (id int primary key , name varchar (50)  , salary int not null );
insert into account values (1  , "axit"  , 5000) , (2 , "yash" , 3000) , (3 , "hari"  , 2300) ;
select * from account ;
select  name , count(salary) from account group by name ;
select  name , avg(salary) from account group by name having avg(salary) > 4000 ;





