# 18) Write a Python program to demonstrate the use of 
# super() in inheritance.

class master:
    def header(self):
        print("This is Header.")
    
    def footer(self):
        print("This is Footer.")

class home(master):
    def header(self):
        return super().header()
    
    def footer(self):
        return super().footer()
    
class about(master):
    def header(self):
        return super().header()
    
    def footer(self):
        return super().footer()
    
h = home()
h.header()
h.footer()

a = about()
a.header()
a.footer()