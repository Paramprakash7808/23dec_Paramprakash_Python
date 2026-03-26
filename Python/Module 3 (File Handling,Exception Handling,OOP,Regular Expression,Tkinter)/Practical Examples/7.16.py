# 16) Write a Python program to show hierarchical inheritance.
# Hierarchical inheritance is Inverse of Multiple Inheritance.

class collage:
    def data(self):
        print("All Student's Data From Collage Method")

class Prakash(collage):
    pid : int
    pFeild : str

    def p_getdata(self):
        self.pid = input("Enter Prakash's Id:")
        self.pFeild = input("Enter Prakash's Feild:")

    def p_printdata(self):
        print("Prakash's Id is:",self.pid)
        print("Prakash's Feild is:",self.pFeild)


class Sahil(collage):
    sid : int
    sFeild : str

    def s_getdata(self):
        self.sid = input("Enter Sahil's Id:")
        self.sFeild = input("Enter Sahil's Feild:")

    def s_printdata(self):
        print("Sahil's Id is:",self.sid)
        print("Sahil's Feild is:",self.sFeild)

class Ajay(collage):
    aid : int
    aFeild : str

    def a_getdata(self):
        self.aid = input("Enter Ajay's Id:")
        self.aFeild = input("Enter Ajay's Feild:")

    def a_printdata(self):
        print("Ajay's Id is:",self.aid)
        print("Ajay's Feild is:",self.aFeild)

p = Prakash()
p.p_getdata()
p.p_printdata()

s = Sahil()
s.s_getdata()
s.s_printdata()

a = Ajay()
a.a_getdata()
a.a_printdata()