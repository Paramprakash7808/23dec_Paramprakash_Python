student = int(input("Enter Number Of Students: "))

data = {}

for i in range(student):
    no = input("Enter Roll No: ")
    name = input("Enter Student's Name: ")
    # print(i)
    # print(data)
    data[no] = name
    # data[name] = name
    
print(data) 