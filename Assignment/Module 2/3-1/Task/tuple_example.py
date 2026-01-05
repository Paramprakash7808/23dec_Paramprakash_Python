names = set()

student = int(input("Enter Number of Students: "))

for i in range(student):
    name = input("Enter Student's Name: ")
    names.add(name)
    # print(name)

print(names)