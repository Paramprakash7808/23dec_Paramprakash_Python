city = ('Rajkot','Ahmedabad','Surat','Baroda','Delhi')

print(city)
print(city[0])
print(city[-1])
print(city[1:3])
print(len(city))

if 'Rajkot' in city:
    print("Yes")
else:
    print("No")

for i in city:
    print(i)

print(city.count('Rajkot'))
print(city.index('Delhi'))

newcity = city
print(newcity)

del city