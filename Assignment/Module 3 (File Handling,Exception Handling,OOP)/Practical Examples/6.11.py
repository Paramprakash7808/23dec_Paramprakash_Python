# 11) Write a Python program to create a class and access the properties 
# of the class using an object.

class data:
    def getdata(self):
        self.id = int(input("Enter Your Id:"))
        self.name = input("Enter Your Name:")
        self.city = input("Enter Your City:")

    def printdata(self):
        print("Your Id is:",self.id)
        print("Your Name is:",self.name)
        print("Your City is:",self.city)

dt = data()
dt.getdata()
dt.printdata()