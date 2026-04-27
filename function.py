# class Student:
#     def __init__(self, name, marks):
#         self.name = name
#         self.marks = marks

#     def display(self):   # instance method
#         print(self.name, self.marks)


# s = Student("Harsh", 90)
# s.display()









# class Student:
#     def __init__(self, name, marks):
#         self.name = name
#         self.marks = marks

#     @classmethod
#     def from_string(cls, data):
#         name, marks = data.split("-")
#         return cls(name, int(marks))


# s = Student.from_string("Harsh-95")
# print(s.name, s.marks)

# class Math:












#     @staticmethod
#     def add(a, b):
#         return a + b


# print(Math.add(2, 3))










# class Student:
#     def __init__(self, marks):
#         self._marks = marks

#     @property
#     def marks(self):
#         return self._marks


# s = Student(90)
# print(s.marks)   # () nahi use kiya












# class Student:
#     def __init__(self, marks):
#         self._marks = marks

#     @property
#     def marks(self):
#         return self._marks

#     @marks.setter
#     def marks(self, value):
#         if value < 0:
#             print("Invalid marks ")
#         else:
#             self._marks = value


# s = Student(90)
# # s.marks = -10   # setter call hoga
# print(s.marks)
# s.marks = 20
# print(s.marks)

































###  inheritance and method overriding




class Animal:
    def sound(self):
        print ("animal sound")


class dog(Animal):
    def sound(self):
        return super().sound()
    def sound(self):
        print("dog braks")


class cat(Animal):
    def sound(self):
        print("cat meaoewww")
    def sound(self):
        return super().sound()
        
    
a = Animal ()
d = dog ()
c = cat ()

c.sound()
d.sound()