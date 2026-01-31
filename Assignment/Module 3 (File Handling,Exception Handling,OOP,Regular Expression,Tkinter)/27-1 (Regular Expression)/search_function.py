import re

mystr = 'This is Python!78778712'

x = re.search('Python',mystr)
print(x)

if x:
    print("Match Found")
else:
    print("No Match Found")