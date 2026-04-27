# class Students:
#     def __init__(self , name , age , marks , rollno ):
#           self.name = name 
#           self.age = age
#           self.marks = marks 
#           self.rollno = rollno
#           self.dict = {"name": self.name, "age": self.age, "marks": self.marks, "rollno": self.rollno}
#     def display_info(self ):
#           print(self.dict)
#     def __str__(self):
#         return f"({self.name} , {self.age} , {self.marks} , {self.rollno})"
    
    
#     def check_passing_marks(self):
#         if self.marks >= 40:
#             return "Passed" 
#         else:   
#             return "Failed"
    
#     # def __repr__(self):
#     #     return f"1234student({self.name} , {self.age} , {self.marks} , {self.rollno})"
          
# s1 = Students("axit" , 20 , 100 , 1)
# s2 = Students("dagara" , 30 , 200 , 1)
# print(s1) 
# print(s2) 
# s1.display_info()
# s2.display_info()
# print(s1.check_passing_marks())
# print(s2.check_passing_marks())




# class car :
#     def __init__(self , name , model , year , color ):
#         self.name = name 
#         self.model = model 
#         self.year = year 
#         self.color = color
#     def display_info(self):
#         print(f"Car Name: {self.name} , Model: {self.model} , Year: {self.year} , Color: {self.color}")
    
#     def change_color(self , new_color):
#         self.color= new_color
#         print(f"Color of the car {self.name} has been changed to {new_color}")


# c1 = car("BMW" , "X5" , 2020 , "Black")
# c2 = car("Audi" , "A4" , 2021 , "White")  
# c1.display_info()
# c2.display_info()   
# c1.change_color("Red")
# c2.change_color("Blue")
# c1.display_info()
# c2.display_info()

# from abc import ABC , abstractmethod

# class Animal(ABC): 
    
#     # def __init__(self   ):
#     #     pass
#     @abstractmethod
#     def sound(self ,  sound="sound"):
#         print (f"animal sound : {sound}")
    
# class dog(Animal):
    
#     # def __init__(self):
#     #     super().__init__()
#     def sound(self):
#         print("dog barks")
#         # return super().sound()
        
        
        
# class cat(Animal):
#     # def __init__(self):
#     #     super().__init__()
#     def sound(self,sound):
#         print(f"cat : {sound}")
#         # return super().sound(sound)
        
        
# cat1 = cat()
# cat1.sound("meows")

# dog1= dog()
# dog1.sound()




# class shape :
#     def area(self) -> None: 
#         print("my shape is diff")



# class curcle(shape):
#     def __init__(self , redius):
#         self.redius = redius
#     def area(self ):
#         my_area = (3.14 *self.redius * self .redius)
#         print (f"my area for this circule : {my_area}")
#         # return print(super().area())
    
    
# class rect(shape):
#     def __init__(self , hight , width):
#         self.hight = hight
#         self.width = width
        
#     def area(self ):
#         my_area = (self.hight * self.width)
#         print(f"my area for this rect:{my_area}")
#         # return print(super().area())


# s1 = curcle(7)
# s2 = rect(10 , 7)

# s1.area()
# s2.area()
    




class employee :
    def saleryyy(self):
        print("it depands on your work type")
    
class fulltime_employee(employee):
    def __init__(self , salary ):
        self.salary = salary
    def saleryyy(self):
        new_salary = self.salary
        print(f"my salary is :{new_salary}")


class parttime_employee(employee): 
    def __init__(self , hr , rate ): 
        self.hr = hr
        self.rate = rate
    
    def saleryyy(self):
        new_salary =  (self.hr *self.rate)
        print(f"my salary is low {new_salary}")
    
    
employee = [ employee() ,fulltime_employee(50000) , parttime_employee(5 , 500)  , fulltime_employee(60000) ] 

for emp in employee:
    emp .saleryyy()
# s1 = fulltime_employee(50000)
# s2 = parttime_employee(5 , 500)


# s1.saleryyy()
# s2.saleryyy()
    
# class paymant:
#     def pay(self , amount):
#         print(f"please mention from which payment {amount} method u can pay")
    
# class UPI(paymant):
#     def pay(self , amount):
#         print(f"paying with UPI {amount}")


# class card(paymant):
#     def pay(self , amount):
#         print(f"paying with card {amount}")


# class cash(paymant):
#     def pay(self , amount):
#         print(f"paying with cash {amount}")
    
# paym = [paymant() , UPI() , card() , cash()]

# for pm in paym :
#     pm.pay(1000)
     
    



class student :
    def __init__(self , name , marks ):
        self.name = name 
        self.marks = marks 
        
    def display(self):
        print(f"display information for studnet with its marks  {self.name} ,,, {self.marks}")
    
    
    def result(self):
        if self.marks >= 40 :
            return "pass" 
        else :
            return "fail"
        
class gredu_student(student):
    def result(self):
        if self.marks >= 70 :
            return "pass" 
        else :
            return "fail"
    
    
students = []



while True:
    print("\n--- Student Management CLI ---")
    print("1. Add Student")
    print("2. View Students")
    print("3. Check Results")
    print("4. Exit")
    
    
    choice = int(input("enter input"))
    
    if choice == 1 :
        name = input("name : ")
        marks = int(input("marks enter : " ))
        
        type_choice = int(input("1 = normal , 2 = gredu_student "))
        if type_choice == 2 :
            std_obj = gredu_student(name , marks )
        else :
            std_obj = student(name , marks)
        
        students.append(std_obj)
    
    elif choice == 2 :
        for s in students :
            s.display()     

    elif choice == 3 :
        print("result")
        for s in students :
            print(f"{s.name} ,,, {s.result()}")
    
    elif choice == 4 :
        print("exiting")
        break
    
    else:
        print("enter valid option")
               

    