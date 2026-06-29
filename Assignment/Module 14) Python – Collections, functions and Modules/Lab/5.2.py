# Write a Python program to access alternate values between index 1 and 5 in a tuple.

# name = ('Prakash','Sahil','Ajay','Mayur','Nik')
# print(name[1:5:2])

# Logic
name = ('Prakash','Sahil','Ajay','Mayur','Nik')

for i in range(1,len(name),2):
    print(name[i])