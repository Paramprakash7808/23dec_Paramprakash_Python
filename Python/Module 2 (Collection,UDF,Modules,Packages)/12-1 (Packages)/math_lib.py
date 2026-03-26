import math

# print("Value of E is:",math.e)
# print("Value of PI is:",math.pi)
# print("Square Root is:",math.sqrt(25))
# print("Value of Ceil is:",math.ceil(25.78))
# print("Value of Floor is:",math.floor(25.78))
# print("Factorial is:",math.factorial(5))
# print("Value of Power is:",math.pow(5,5))

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