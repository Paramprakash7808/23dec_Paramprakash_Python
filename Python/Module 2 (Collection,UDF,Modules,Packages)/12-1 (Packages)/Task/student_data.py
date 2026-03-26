import random,datetime

student = int(input("Enter number of Students:"))

s = []

def data():
    name = input("Enter Your Name:")
    city = input("Enter Your City:")
    time = datetime.datetime.now()
    id = random.randint(1,1000)
    s.append([name,city,time,id])

for i in range(student):
    data()

for i in s:
    print("Your Name is:",i[0])
    print("Your City is:",i[1])
    print("Time is:",i[2])
    print("Id is:",i[2])

# student = int(input("Enter Number of Students:"))

# # s = []

# def data():
#     name = input("Enter Your Name:")
#     city = input("Enter Your City:")
#     time = datetime.datetime.now()
#     id = random.random()

#     print("Your Name is:",name)
#     print("Your Id is:",id)

# for i in range(student):
#     data()

# # for student in s:
# #     # print("Your Name is:",name)
# #     # print("Your Id is:",id)
# #     print(student)