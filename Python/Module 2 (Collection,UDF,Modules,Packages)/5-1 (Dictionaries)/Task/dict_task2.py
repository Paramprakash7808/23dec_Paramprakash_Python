student = int(input("Enter Number Of Students: "))

data = {}

for i in range(student):
    id = int(input("Enter Your Id:"))
    name = input("Enter Your Name:")
    city = input("Enter Your City:")

    data[id] = {"Your Name is":name,"Your City is":city}

for i in data.items():
    print(i)