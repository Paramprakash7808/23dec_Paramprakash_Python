# def data(id,name,city):
#     print("Your Id is:",id)
#     print("Your Name is:",name)
#     print("Your City is:",city)

# data(1,'Rajkot','Prakash') #Positional Argument(Static Data)

# data(id=1,city='Rajkot',name='Prakash') #Keyword Argument(Static Data)

def data(id,name,city):
    print("Your Id is:",id)
    print("Your Name is:",name)
    print("Your City is:",city)

id = int(input("Enter Your Id:"))
name = input("Enter Your Name:")
city = input("Enter Your City:")

data(id,name,city) #Dynamic Data