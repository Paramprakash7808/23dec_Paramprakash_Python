import re

mystr = 'This is Python!78778712'

# x = re.findall('^This',mystr) # cap(^) Only Check Starting First Word
# x = re.findall('^[A-Z]',mystr)
x = re.findall('12$',mystr) # $ Only Check at the end last Word
print(x)