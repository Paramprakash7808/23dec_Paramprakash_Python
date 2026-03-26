student = int(input("Enter Number of Students: "))

info = []

# id = int(input("Enter Your Id:"))
# name = input("Enter Your Name:")
# city = input("Enter Your City:")

def data(id,name,city):
    print("Your Id is:",id)
    print("Your Name is:",name)
    print("Your City is:",city)

for i in range(student):
    id = int(input("Enter Your Id:"))
    name = input("Enter Your Name:")
    city = input("Enter Your City:")
    # print(i)
    info.append((id,name,city))

for i in info:
    print(i)