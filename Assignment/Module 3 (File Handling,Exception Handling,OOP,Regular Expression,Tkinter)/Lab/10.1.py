# Write a Python program to search for a word in a string using re.search().

import re

mystr = 'This is Python!78778712'

x = re.search('Python',mystr)
print(x)

if x:
    print("Match Found",x.group()) # group method print matched word
else:
    print("No Match Found")