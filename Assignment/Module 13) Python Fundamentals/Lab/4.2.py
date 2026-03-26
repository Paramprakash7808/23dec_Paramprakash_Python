# Practical Example 6: Write a Python program to check if a number is prime using if_else.

num = int(input("Enter a number: "))

if num == 2:
    print("Prime number")
elif num <= 1:
    print("Not a prime number")
elif num % 2 == 0:
    print("Not a prime number")
else:
    print("Prime number")