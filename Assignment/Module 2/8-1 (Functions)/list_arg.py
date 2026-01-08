# def info(data):
#     print("Your Id is:",data[0])
#     print("Your Name is:",data[1])
#     # print("Your City is:",data[2]) 

# info([101,'Prakash','Rajkot']) # List Argument(Static Data)

def info(data):
    print("Your Id is:",data[0])
    print("Your Name is:",data[1])
    print("Your City is:",data[2])

x = int(input("Enter Your Id: "))
y = input("Enter Your Name: ")
z = input("Enter Your City: ")

info([x,y,z]) # List Argument(Dynamic Data)