# 7) Write a Python program to handle exceptions in a calculator.

try:
    a = int(input("Enter Value Of A:"))
    b = int(input("Enter Value Of B:"))

    print("Addition of A and B is:", a + b)
    print("Subtraction of A and B is:", a - b)
    print("Multiplication of A and B is:", a * b)
    print("Division of A and B is:",a/b)
    
except ZeroDivisionError:
    print("Can not Divisible by 0")
except ValueError:
    print("Invalid Input")