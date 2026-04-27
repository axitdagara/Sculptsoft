
"""a = float(input("enter value : "))
o = input(" enter valid operator : ")
b = float(input("enter value : "))

if o == '+':
    print(a + b)
elif o == '-':
    print(a - b)
elif o == '*':
    print(a * b)
elif o == '/':
    if b == 0:
        print("Cannot divide by zero")
    else:
        print(a / b)
else:
    print("Invalid Operator")
"""


a = float(input("Enter first number: "))
b = float(input("Enter second number: "))
o = input("Enter operator (+, -, *, /): ")

calc = {
    "+": a + b,
    "-": a - b,
    "*": a * b,
    "/": a / b 
     if b != 0 else "Error: Division by zero"
}
print(f"Result: {calc.get(o, 'Invalid Operator')}")








    

    


