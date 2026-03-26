# 8) 
# Write a Python program to handle multiple exceptions (e.g., file not found, division by zero).

try:
    fi = open('data.txt','r')
    print(fi.read())
    a = int(input("Enter Value Of A:"))
    b = int(input("Enter Value Of B:"))

    print("Division of A and B is:",a/b)

except FileNotFoundError:
    print("File Not Found")

except ZeroDivisionError:
    print("Can not Divisible by 0")

except ValueError:
    print("Invalid Input")