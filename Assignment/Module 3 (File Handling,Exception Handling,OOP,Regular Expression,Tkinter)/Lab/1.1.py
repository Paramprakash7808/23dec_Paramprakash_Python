# Write a Python program to print a formatted string using print() and f-string.

# Using print
print('Using Print')
id = int(input("Enter Your ID:"))
name = input("Enter Your Name:")
city = input("Enter Your City:")
print("Your ID is: {},\nYour Name is: {},\nYour City is: {}".format(id,name,city))

# Using f-string
print("Using f-string")
id = int(input("Enter Your ID:"))
name = input("Enter Your Name:")
city = input("Enter Your City:")
print(f"Your ID is: {id}\nYour Name is: {name}\nYour City is: {city}")