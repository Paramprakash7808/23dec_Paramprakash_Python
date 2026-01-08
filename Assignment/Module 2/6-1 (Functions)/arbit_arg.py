# def data(*data):
#     print("Your Id is:",data[0])
#     print("Your Name is:",data[1])
#     print("Your City is:",data[2])

# data(1,'Prakash','Rajkot') #Static Data

def data(*data):
    print("Your Id is:",data[0])
    print("Your Name is:",data[1])
    print("Your City is:",data[2])

x = int(input("Enter Your Id:"))
y = input("Enter Your Name:")
z = input("Enter Your City:")

data(x,y,z) #Dynamic Data