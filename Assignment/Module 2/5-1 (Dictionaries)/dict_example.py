stdata = {
    'id' : 1,
    'name' : 'Prakash',
    'city' : 'Rajkot'
}

print(stdata)
print(stdata['name'])
print(stdata.get('id'))
print(stdata.keys())
print(stdata.values())
print(len(stdata))

if 'city' in stdata:
    print("Yes")
else:
    print("No")

if 'Prakash' in stdata.values():
    print("Yes")
else:
    print("No")

for i in stdata:
    print(i)

for i in stdata.values():
    print(i)

for i in stdata.items():
    print(i)

stdata['id'] = 2
print(stdata)

stdata['subject'] = 'Python'
print(stdata)

stdata['city'] = 'Tithava'
print(stdata)

stdata.pop('city')
print(stdata)

newdata = stdata.copy()
print(newdata)

stdata.clear()
print(stdata)