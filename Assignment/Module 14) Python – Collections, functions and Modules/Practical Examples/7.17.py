# 17) Write a Python program to convert two lists into one 
# dictionary using a for loop.

list1 = ['id', 'name', 'city']
list2 = [1, 'Prakash', 'Rajkot']

data = {}

for i in range(len(list1)):
    data[list1[i]] = list2[i]

print(data)