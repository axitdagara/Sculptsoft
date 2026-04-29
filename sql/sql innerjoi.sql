create database if not exists studs ;
use studs ;
create table stud_ifo (id int , name varchar (50)) ;
create table stud_ifoo (id int , s_name varchar (50)) ;
insert into stud_ifo values (1 , "axit") , (2 , "yash ") , (3 , "hari");
insert into stud_ifoo values (1 , "dagara") , (2 , "soni ") , (4 , "kaka");


select name,s_name from stud_ifo inner join stud_ifoo on stud_ifo.id = stud_ifoo.id ;
select * from stud_ifo inner join stud_ifoo on stud_ifo.id = stud_ifoo.id ;
select * from stud_ifo left join stud_ifoo on stud_ifo.id = stud_ifoo.id ;




select stud_ifo.id ,name,s_name from stud_ifo inner join stud_ifoo on stud_ifo.id = stud_ifoo.id ;
select stud_ifo.id ,name,s_name from stud_ifo left join stud_ifoo on stud_ifo.id = stud_ifoo.id ;
select stud_ifo.id ,name,s_name from stud_ifo right join stud_ifoo on stud_ifo.id = stud_ifoo.id ;
select stud_ifo.id ,name,s_name from stud_ifo left join stud_ifoo on stud_ifo.id = stud_ifoo.id union select stud_ifo.id ,name,s_name from stud_ifo right join stud_ifoo on stud_ifo.id = stud_ifoo.id ;
select * from stud_ifo left join stud_ifoo on stud_ifo.id = stud_ifoo.id where stud_ifoo.id is null ;
select * from stud_ifo right join stud_ifoo on stud_ifo.id = stud_ifoo.id where stud_ifo.id is null ;
select * from stud_ifo left join stud_ifoo on stud_ifo.id = stud_ifoo.id where stud_ifoo.id is null union select * from stud_ifo right join stud_ifoo on stud_ifo.id = stud_ifoo.id where stud_ifo.id is null ;


create table mentor (id int , name varchar(50) , p_id int);
insert into mentor values (1 , "axit" , null) , (2 , "yash" , 1) , (3 , "hari" , 2) ;

select s1.name as mentor_name , s2.name as name from mentor as s1 join mentor as s2 where s1.id = s2.p_id ;
select s1.name  , s2.name from mentor as s1 join mentor as s2 where s1.id = s2.p_id ;

 
 
 