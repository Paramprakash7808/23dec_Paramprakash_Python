# Practical Example: 9) Write a Python program to print every alternate character from the
# string starting from index 1.

mystr = "This is Python!"

for i in range(1, len(mystr), 2):
    print(mystr[i], end="")