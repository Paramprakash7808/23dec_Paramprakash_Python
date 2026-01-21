# n = int(input("Enter Number of Students:"))

# students = []

# class data():
#     id : int
#     name : str

#     def getdata(self):
#         self.id = input("Enter Your Id:")
#         self.name = input("Enter Your Name:")

#     def printdata(self):
#         print("Your Id is:",self.id)
#         print("Your Name is:",self.name)

# for i in range(n):
#         dt = data()
#         dt.getdata()
#         students.append(dt)

# for dt in students:
#      dt.printdata()


class data():
    id : int
    name : str
    
    def getdata(self):
        n = int(input("Enter Number of Students:"))

        fi = open('data.txt','a')
        for i in range(n):
            self.id = input("Enter Your Id:")
            self.name = input("Enter Your Name:")

            fi.write(f"Your Id is: {self.id}\n")
            fi.write(f"Your Name is: {self.name}\n\n")
        fi.close()

    def printdata(self):
        fi = open("data.txt",'r')
        print(fi.read())

dt = data()
print("Enter 1 For Insert Data")
print("Enter 2 For Read Data")
choice = int(input("Enter Your Choice:"))

if choice == 1:
    dt.getdata()
elif choice == 2:
    dt.printdata()