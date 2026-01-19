fi = open('temp.txt','a')

id = input("Enter an ID:")
name = input("Enter Your Name:")
city = input("Enter Your City:")

fi.write(f'Your ID is: {id}\nYour Name is: {name}\nYour City is: {city}')
fi.write("\n--------------------------\n")