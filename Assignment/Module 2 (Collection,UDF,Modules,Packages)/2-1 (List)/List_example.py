sub = ['c','c++','sql','python']
print(sub)

print(sub[0])
print(sub[-1])
print(sub[0:2])
print(sub[:3])
print(sub[2:])

print(len(sub))

if 'sql' in sub:
    print("Yes")
else:
    print("No")

for i in sub:
    print(i)

print(sub.index('sql'))

sub[2] = 'dbms'
print(sub)

sub.append('sql')
print(sub)

sub.insert(4,'html')
print(sub)

sub.remove('dbms')
print(sub)

sub.pop()
print(sub)

sub.pop(1)
print(sub)

# sub.clear()
# print(sub)

# del sub
# print(sub)

sub.sort()
print(sub)

sub.reverse()
print(sub)

newsub = sub.copy()
print(newsub)

newsub = ['css','js']
print(newsub)

print(sub+newsub)

sub.extend(newsub)
print(sub)