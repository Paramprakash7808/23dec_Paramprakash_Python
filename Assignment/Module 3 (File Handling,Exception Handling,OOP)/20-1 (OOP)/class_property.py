class data():
    id : int
    name : str

    def getdata(self):
        self.id = input("Enter Your Id:")
        self.name = input("Enter Your Name:")

    def printdata(self):
        print("Your Id is:",self.id)
        print("Your Name is:",self.name)

dt = data()
dt.getdata()
dt.printdata()