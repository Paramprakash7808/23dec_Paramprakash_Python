fi = open('temp.txt','w')

id = input("Enter an ID:")
name = input("Enter Your Name:")
city = input("Enter Your City:")

# fi.write(id)
# fi.write(name)
# fi.write(city)

fi.write(f'Your ID is: {id}\nYour Name is: {name}\nYour City is: {city}')