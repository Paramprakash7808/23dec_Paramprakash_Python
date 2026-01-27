# Write a Python program to demonstrate handling multiple exceptions.

try:
    a = int(input("Enter Value Of A:"))
    b = int(input("Enter Value Of B:"))

    print("Division of A and B is:",a/b)
    
except ZeroDivisionError:
    print("Can not Divisible by 0")
except ValueError:
    print("Invalid Input")