# 17) Write a Python 
# program to show hybrid inheritance.
# hybrid inheritance is Inverse of Multilevel Inheritance.
# Hybrid inheritance is a combination of two or more types of inheritance.

# 14) Write a 
# Python program to show multilevel inheritance.

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

class Ajay(Prakash):
    aid : int
    aFeild : str

    def a_getdata(self):
        self.aid = input("Enter Ajay's Id:")
        self.aFeild = input("Enter Ajay's Feild:")

class collage(Sahil,Ajay):
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