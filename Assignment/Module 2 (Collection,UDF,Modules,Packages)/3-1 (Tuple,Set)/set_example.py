myset = {'a','b','c','d','e'}

print(myset)

if 'c' in myset:
    print("Yes")
else:
    print("No")

print(len(myset))

for i in myset:
    print(i)

# Methods:
myset.add('f')
print(myset)

myset.update(['f','g','h'])
print(myset)

myset.pop()
print(myset)

# myset.clear()
# print(myset)

newset = myset.copy()
print(newset)

newset = {'p','q','r','s','t','a','c'}
print(newset)

x = myset.union(newset)
print(x)

y = myset.intersection(newset)
print(newset)