import re

email = input("Enter Your Email:")
email_pattern = "[a-z0-9]+[@]+[a-z]+[\.]+[a-z]"

x = re.findall(email_pattern,email)

if x:
    print("Email is Valid")
else:
    print("Invalid Email")