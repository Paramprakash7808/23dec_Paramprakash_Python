# 24) Write a Python program to match a word in a string using re.match().

import re

mystr = 'This is Python!78778712'

x = re.match('This',mystr)
print(x)

if x:
    print("Match Found",x.group()) # group method print matched word
else:
    print("No Match Found")