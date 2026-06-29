# Practical Example: 1) Write a Python program to skip 'banana' in a list using the continue statement. List1 = ['apple', 'banana', 'mango']

List1 = ['apple', 'banana', 'mango']

for i in List1:
    if i == "banana":
        continue
    print(i)