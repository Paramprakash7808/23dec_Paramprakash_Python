# def data(id,name,city='Rajkot'):
#     print("Your Id is:",id)
#     print("Your Name is:",name)
#     print("Your City is:",city)

# data(1,'Prakash') # Static Data
# data(1,'Prakash','Ahmedabad') #Static Data

def data(id,name,city='Rajkot'):
    print("Your Id is:",id)
    print("Your Name is:",name)
    print("Your City is:",city)

id = int(input("Enter Your Id:"))
name = input("Enter Your Name:")
city = input("Enter Your City:")

data(id,name,city) #Dynamic Data