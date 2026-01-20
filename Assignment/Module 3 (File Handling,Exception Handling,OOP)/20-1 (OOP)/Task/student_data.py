n = int(input("Enter Number of Students:"))

students = []

class data():
    id : int
    name : str

    def getdata(self):
        self.id = input("Enter Your Id:")
        self.name = input("Enter Your Name:")

    def printdata(self):
        print("Your Id is:",self.id)
        print("Your Name is:",self.name)

for i in range(n):
        dt = data()
        dt.getdata()
        students.append(dt)

for dt in students:
     dt.printdata()