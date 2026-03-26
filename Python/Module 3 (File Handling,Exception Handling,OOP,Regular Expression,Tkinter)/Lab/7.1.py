# Write Python programs to demonstrate different types of inheritance (single, multiple, 
# multilevel, etc.).

print("Single inheritance:")
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

print("Multiple Inheritance:")
class Prakash:
    pid : int
    pFeild : str

    def p_getdata(self):
        self.pid = input("Enter Prakash's Id:")
        self.pFeild = input("Enter Prakash's Feild:")

class Sahil:
    sid : int
    sFeild : str

    def s_getdata(self):
        self.sid = input("Enter Sahil's Id:")
        self.sFeild = input("Enter Sahil's Feild:")

class Ajay:
    aid : int
    aFeild : str

    def a_getdata(self):
        self.aid = input("Enter Ajay's Id:")
        self.aFeild = input("Enter Ajay's Feild:")

class collage(Prakash,Sahil,Ajay):
    def printdata(self):
        print("Prakash's Id is:",self.pid)
        print("Prakash's Feild is:",self.pFeild)
        print("Sahil's Id is:",self.sid)
        print("Sahil's Feild is:",self.sFeild)
        print("Ajay's Id is:",self.aid)
        print("Ajay's Feild is:",self.aFeild)

clg = collage()
clg.p_getdata()
clg.s_getdata()
clg.a_getdata()
clg.printdata()

print("Multilevel Inheritance:")
class Prakash:
    pid : int
    pFeild : str

    def p_getdata(self):
        self.pid = input("Enter Prakash's Id:")
        self.pFeild = input("Enter Prakash's Feild:")

class Sahil(Prakash):
    sid : int
    sFeild : str

    def s_getdata(self):
        self.sid = input("Enter Sahil's Id:")
        self.sFeild = input("Enter Sahil's Feild:")

class Ajay(Sahil):
    aid : int
    aFeild : str

    def a_getdata(self):
        self.aid = input("Enter Ajay's Id:")
        self.aFeild = input("Enter Ajay's Feild:")

class collage(Ajay):
    def printdata(self):
        print("Prakash's Id is:",self.pid)
        print("Prakash's Feild is:",self.pFeild)
        print("Sahil's Id is:",self.sid)
        print("Sahil's Feild is:",self.sFeild)
        print("Ajay's Id is:",self.aid)
        print("Ajay's Feild is:",self.aFeild)

clg = collage()
clg.p_getdata()
clg.s_getdata()
clg.a_getdata()
clg.printdata()