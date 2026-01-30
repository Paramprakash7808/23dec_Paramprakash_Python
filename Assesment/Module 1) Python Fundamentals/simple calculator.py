# Create a mini-project where students combine conditional statements, loops, and functions 
# to create a basic Python application, such as a simple calculator or a grade management 
# system.

# simple calculator

def add(a,b):
    return a+b

def sub(a,b):
    return a-b

def mul(a,b):
    return a*b

def div(a,b):
    return a/b

def mod(a,b):
    return a%b

while True:
    print("Enter 1 for Addition \nEnter 2 for Subtraction \nEnter 3 for Multiplication \nEnter 4 for Division \nEnter 5 for Modules \nEnter 6 for Exit")

    choice = int(input("Enter Your Choice:"))

    if choice == 6:
        print("Exit")
        break

    no1 = int(input("Enter 1st No:"))
    no2 = int(input("Enter 2nd No:"))

    if choice == 1:
        print("Addition of 1st and 2nd Number is:",add(no1,no2))
    elif choice == 2:
        print("Subtraction of 1st and 2nd Number is:",sub(no1,no2))
    elif choice == 3:
        print("Multiplication of 1st and 2nd Number is:",mul(no1,no2))
    elif choice == 4:
        print("Division of 1st and 2nd Number is:",div(no1,no2))
    elif choice == 5:
        print("Modules of 1st and 2nd Number is:",mod(no1,no2))
    else:
        print("Invalid Choice")