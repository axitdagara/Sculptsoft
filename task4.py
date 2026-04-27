"""
f_name = input("Enter your full name: ")
print(f"Uppercase: {f_name.upper()}")
print(f"Lowercase: {f_name.lower()}")
print(f"Title Case: {f_name.title()}")

vowels = "aeiouAEIOU"
vowel_count = sum(1 for i in f_name if i in vowels)
print(f"Number of vowels: {vowel_count}")

reversed_name = f_name[::-1]
print(f"Reversed Name: {reversed_name}")
"""
#vowel_count = sum(map(f_name.lower().count, "aeiou"))







# while True: 
#      try:
#         i= float(input("Enter your score (0-100): "))
#         if 0 <= i <= 100:
#             if i >= 90:
#                 grade = "A"
#             elif i >= 80:
#                 grade = "B"
#             elif i >= 70:
#                 grade = "C"
#             elif i >= 60:
#                 grade = "D"
#             else:
#                 grade = "F"
#             print(f"Your grade is: {grade}")
#         else:
#             print("Please enter a valid score between 0 and 100.")
#      except ValueError:
#         print("Invalid input. Please enter a number.")











# i = int(input("Enter a number: "))
# is_prime = True

# for j in range(2, i):
#     if i % j == 0:
#         is_prime = False
#         break

# if is_prime and i > 1:
#     print(f"{i} is a prime number.")
# else:
#     print(f"{i} is not a prime number.")
    
    
 
 
 
 
 
 
 
 
 
 
 
"""def is_palindrome(s):
    str1= s.replace(" ", "").lower()
    str1 = ''.join(char for char in str1 if char.isalnum())
    return str1 == str1[::-1]


test_cases = [
    "A man a plan a canal Panama",
    "racecar",
    "hello",
    "Was it a car or a cat I saw?",
    "12321",
    "Python",
    "A man a plan a canal Panama" 
    
]

print("\n Palindrome ")
for case in test_cases:
    print(f"'{case}': {is_palindrome(case)}")"""
    
    
    
"""import time 
    
    
n= int(input("enter value : "))    
def fact_i(n):
        if n < 0:
            return "Error: Negative input"
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
def fact_re(n):
        if n < 0:
            return "Error: Negative input"
        if n == 0 or n == 1:
            return 1
        return n * fact_re(n - 1)
    
def compare(n):
        if n < 0:
            print("Please enter a non-negative integer.")
            return
    
        
        fact_i(n)
        iter_result = fact_i(n)
    
        
        try:
            recur_result = fact_re(n)
        except RecursionError:
            recur_result = "Failed (Recursion Depth Exceeded)"
    
        
        print(f"Iterative result: {iter_result}")
        print(f"Recursive result: {recur_result}")
       
        if iter_result == recur_result:
            print("Both methods produced the same result.") 
    
       
    
        start_time = time.time()
        fact_i(n)
        end_time = time.time()
        i_time = end_time - start_time
    
        start_time = time.time()
        fact_re(n)
        end_time = time.time()
        r_time = end_time - start_time
    
        print(f"Time taken by  method1: {i_time:.6f} seconds")
        print(f"Time taken by  method2: {r_time:.6f} seconds")
    
compare(n)
    
   

    """
    





# import random
# random_List = [random.randint(1, 100) for i in range(10)]
# print(f"Random List: {random_List}")  
                  
# min_value = min(random_List)
# max_value = max(random_List)                    
# average = sum(random_List) / len(random_List)       
# print(f"Min: {min_value}")
# print(f"Max: {max_value}")                      
# print(f"Ave: {average: .2f}")                                                    
# uniq_list = []                                                                
# for n in random_List:
#     if n not in uniq_list:
#         uniq_list.append(n)                             
# print(f"without duplicates: {uniq_list}")                
# sorted_list_asc = sorted(uniq_list)
# sorted_list_desc = sorted(uniq_list, reverse=True)                
# print(f"Sorted (asc): {sorted_list_asc}")        
# print(f"Sorted (desc): {sorted_list_desc}")  




# inventory = {}

# def add_item(name:str, quantity:int):
#     inventory[name]= quantity
#     print(f"Added {name}: {quantity}")

# def update_item(name:str, quantity:int):
#     if name in inventory:
#         inventory[name] = quantity
#         print(f"Updated {name} to {quantity}")
#     else:
#         print(f"{name} not found")

# def remove_item(name:str):
#     if name in inventory:
#         del inventory[name]
#         print(f"Removed {name}")
#     else:
#         print(f"{name} not found")

# def display_inventory():
#     if inventory:                                                     
#         print("\nInventory:")
#         for name, quantity in inventory.items():
#             print(f"  {name}: {quantity}")
#     else:
#         print("Inventory is empty")

# add_item("Apples", "10")
# add_item("Oranges", 15)
# add_item("Grapes", 20)

# add_item("Bananas", 5)
# ##update_item("Apples", 15)
# ##remove_item("Bananas")
# display_inventory()





    
def text_file_processor():
       
        filename = "sample.txt"
      
        f = open(filename, "w")
        print("Enter 5 sentences:")
        for i in range(5):
            sentence = input(f"Sentence {i+1}: ")
            f.write(sentence + "\n")
        f.close()
      
        f = open(filename, "r")
        lines = f.readlines()
        f.close()
        
        line_count = len(lines)
        total_words = sum(len(line.split()) for line in lines)
        print(f"Total lines: {line_count}")
        print(f"Total words: {total_words}")
        
      
        f = open("reversed.txt", "w")
        for line in reversed(lines):
            f.write(line)
       
     
                          
        f.close()

text_file_processor()

                        
                        
                        
                        
    
    
    
    
    
    
                        
                        
# class nagetiveNumberError(Exception):
#     pass                        
# class nonIntegerError(Exception):
#     pass                                  
                    
# while True:
#     try:
#         num = input("Enter an integer: ")
#         if num < 0:
#             raise nagetiveNumberError("Negative numbers are not allowed.")
#         elif not num.isdigit():
#             raise nonIntegerError("Input must be an integer.")
#         elif num == 0:
#             print("0 is neither even nor odd.")      
#         elif int(num) % 2 == 0:
#             print(f"{num} is even.")
#         else:
#             print(f"{num} is odd.")
#         break
#     except nagetiveNumberError as e:
#         print(e)
#     except nonIntegerError as e:
#         print(e)





                           
                            
                            
                            
                            
                            
                