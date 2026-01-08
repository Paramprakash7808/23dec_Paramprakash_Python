# def data(id,name):
#     return id,name

# def info():
#     x = data(101,'Prakash') # Static Data
#     print("Your Id is:",x[0])
#     print("Your Name is:",x[1])

# info()

def data(id,name):
    return id,name

x = int(input("Enter Your Id:"))
y = input("Enter Your Name:")

def info():
    print("Your Id is:",x)
    print("Your Name is:",y)
    z = data(x,y) # Dynamic Data

info()