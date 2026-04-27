# nums = [1,2,3,4]

# square_dict = {i: i*i for i in nums}
# print(square_dict.keys())
# print(square_dict.items())


# num = {"a":1 , "b":2 }
# print(num.items())



# try:
#     x = int("abc")
# except ValueError:
#     print("Wrong value diya hai")

    
    
# f = open ("my.txt" , "w")
# f.write("good moring")
# f.close()


# with open("my.txt", "a") as f:
#     f.write("\nNew Line added")
    

# with open("my.txt" , "r") as f:
#     data = f.read()
#     print(data)
#     split = data.split()
#     print(split)
#     print(data.__len__())
#     print(split.count("o"))
    
 
 
# class Math:

#     @staticmethod
#     def add(a, b):
#         return a + b

# print(Math.add(2, 3))



# class Student:
#     school = "ABC School"

#     @classmethod
#     def get_school(cls):
#         return cls.school


# print(Student.get_school())


import requests

response = requests.get("https://api.github.com")

print(response.status_code)
print(response.json())
print(response.request)