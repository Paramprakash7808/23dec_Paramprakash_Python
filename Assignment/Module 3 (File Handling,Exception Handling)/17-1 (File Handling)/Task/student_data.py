fi = open('data.txt','a')

n = int(input("Enter Number Of Students:"))

for i in range(n):
    id = int(input("Enter an ID:"))
    name = input("Enter a Name:")
    city = input("Enter a City:")
    fi.write(f"\nYour Id is: {id}\n Your Name is: {name}\n Your City is: {city}\n")