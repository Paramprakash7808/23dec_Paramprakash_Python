import re

username = input("Enter Your UserName:")
username_pattern = '[A-Z]+[a-z]+[0-9]+'

x = re.findall(username_pattern,username)
print(x)

if x:
    print("Valid UserName")
else:
    print("Invalid UserName")