
full_name = input("Enter your full name: ")

print(f"Uppercase: {full_name.upper()}")
print(f"Lowercase: {full_name.lower()}")
print(f"Title Case: {full_name.title()}")

vowels = "aeiouAEIOU"
vowel_count = sum(1 for char in full_name if char in vowels)
print(f"Number of vowels: {vowel_count}")

reversed_name = full_name[::-1]
print(f"Reversed Name: {reversed_name}")


















# Task 2: Grade Calculator
while True:
    try:
        score = float(input("Enter the student's score (0-100): "))
        if 0 <= score <= 100:
            break
        else:
            print("Invalid input. Please enter a score between 0 and 100.")
    except ValueError:
        print("Invalid input. Please enter a numeric value.")

# Grade logic
if score >= 90:
    grade = 'A'
elif score >= 80:
    grade = 'B'
elif score >= 70:
    grade = 'C'
elif score >= 60:
    grade = 'D'
else:
    grade = 'F'

print(f"Score: {score}, Grade: {grade}")


















import time

def factorial_iterative(n):
    if n < 0:
        return "Error: Negative input"
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def factorial_recursive(n):
    if n < 0:
        return "Error: Negative input"
    if n == 0 or n == 1:
        return 1
    return n * factorial_recursive(n - 1)

# Performance Comparison
def compare_performance(n):
    if n < 0:
        print("Please enter a non-negative integer.")
        return

    # Iterative Timing
    start = time.perf_counter()
    factorial_iterative(n)
    end = time.perf_counter()
    iter_time = end - start

    # Recursive Timing
    start = time.perf_counter()
    try:
        factorial_recursive(n)
        end = time.perf_counter()
        recur_time = end - start
    except RecursionError:
        recur_time = "Failed (Recursion Depth Exceeded)"

    print(f"--- Performance for n={n} ---")
    print(f"Iterative: {iter_time:.8f} seconds")
    print(f"Recursive: {recur_time if isinstance(recur_time, str) else f'{recur_time:.8f} seconds'}")

# Example Usage
compare_performance(500)

















number = 7
guess = int(input("Guess a number between 1 and 10: "))
    
if guess == number:
        print("You got it right!")
else:
        print(f"Wrong! The number was {number}")

    





import re

def is_palindrome(s):
    # Remove all non-alphanumeric characters and convert to lowercase
    clean_s = re.sub(r'[^a-zA-Z0-0]', '', s).lower()
    
    # Compare string with its reverse
    return clean_s == clean_s[::-1]

# Testing
test_cases = [
    "A man a plan a canal Panama", # True
    "racecar",                     # True
    "hello",                       # False
    "Was it a car or a cat I saw?",# True
    "12321",                       # True
    "Python"                       # False
]

print("--- Palindrome Test Results ---")
for text in test_cases:
    print(f"'{text}': {is_palindrome(text)}")













import math

# Take input from the user
num = int(input("Enter a number: "))

if num > 1:
    is_prime = True
    # Optimize by checking divisibility up to the square root of num
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            is_prime = False
            break
            
    if is_prime:
        print(f"{num} is a prime number.")
    else:
        print(f"{num} is not a prime number.")
else:
    # Numbers less than or equal to 1 are not prime
    print(f"{num} is not a prime number.")
