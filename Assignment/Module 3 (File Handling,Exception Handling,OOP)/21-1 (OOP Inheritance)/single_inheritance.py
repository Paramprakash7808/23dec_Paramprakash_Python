class father:
    bal : int
    car : int

    def getdata(self):
        self.bal = input("Enter Balance:")
        self.car = input("Enter Number Of Cars:")

class son(father):
    def printdata(self):
        print("Father's Balance is:",self.bal)
        print("Father's Cars is:",self.car)

sn = son()
sn.getdata()
sn.printdata()