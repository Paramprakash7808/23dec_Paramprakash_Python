# Write Python programs to demonstrate method overloading and method overriding.

print("Method Overloading")
class data:
    # Method Overloading
    def getdata(self,id):
        print("Your Id is:",id)

    def getdata(self,name):
        print("Your Name is:",name)

dt = data()
dt.getdata("Prakash")


print("\nMethod Overriding")
class master:
    def header(self):
        print("This is Header")

    def footer(self):
        print("This is Footer")

class home(master):
    def header(self): # overridden
        print("This is Home Page")
    
class about(master):
    def header(self): # overridden
        print("This is About Page")
    
m = master()
m.header()
m.footer()

h = home()
h.header()
h.footer()

a = about()
a.header()
a.footer()