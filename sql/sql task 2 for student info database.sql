create database student_records ;
use student_records ;
create table if not exists students (
                    id int primary key , 
                    name varchar (50) );
create table if not exists courses (
					id int primary key ,
                    c_name varchar (50) ,
                    department varchar (50));
                    
insert into students values (1, "axit") ,
                             (2 , "harsh") ,
                             (3 , "jaydeep") , 
                             (4 , "meet") ,
                             (5 , "pratham ") ;
insert into courses values (1 , "it" , "iot") , 
                          (2 , "it" ,"iot") ,
                          (3 ,"bd" , "bspp") ,
                          (4 ,"aiml" ,"bspp" ) ,
						(5 ,"ce", "iot") ;
                        
insert into courses value (6 , "it" , "iot");
                             
                    
				
select * from students left join courses on students.id = courses.id ;
select * from students right join courses on students.id = courses.id ;
select * from students inner join courses on students.id = courses.id ;

	
