# Write a Python program to create a calculator using functions. 

no1 = int(input("Enter 1st No: "))
no2 = int(input("Enter 2nd No: "))

def calc(no1,no2):
    print("Addition of 1st and 2nd Number is:",no1+no2)
    print("Subtraction of 1st and 2nd Number is:",no1-no2)
    print("Multiplication of 1st and 2nd Number is:",no1*no2)
    print("Division of 1st and 2nd Number is:",no1/no2)
    print("Modulus of 1st and 2nd Number is:",no1%no2)

calc(no1,no2)