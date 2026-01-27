import re

mystr = 'This is Python!78778712'

x = re.match('This',mystr)
print(x)

if x:
    print("Match Found")
else:
    print("No Match Found")