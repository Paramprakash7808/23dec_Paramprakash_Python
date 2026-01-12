# 23) Write a Python program to demonstrate the use of functions from 
# the math module.

import math

square = int(input("Enter Value for Square Root:"))
print("Square Root is:",math.sqrt(square))

fact = int(input("Enter Value for Factorial:"))
print("Factorial is:",math.factorial(fact))

ceil = float(input("Enter Value for Ceil:"))
print("Ceil is:",math.ceil(ceil))

floor = float(input("Enter Value for Floor:"))
print("Floor is:",math.floor(floor))

power1 = int(input("Enter 1st Number for Power:"))
power2 = int(input("Enter 2nd Number for Power:"))
print("Power is:",math.pow(power1,power2))