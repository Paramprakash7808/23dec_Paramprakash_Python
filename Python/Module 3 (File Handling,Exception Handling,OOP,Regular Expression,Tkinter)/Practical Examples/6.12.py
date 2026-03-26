# 12) Write a Python program to demonstrate the use of local and 
# global variables in a class.

id = 101 #Global Variable
name = 'Prakash' #Global Variable

class local:
    def globalexample(self):
        print("From Global Variable")
        print("Your Id is:",id)
        print("Your Name is:",name)

    def localexample(self):
        id = 102 #Local Variable
        name = 'Meet' #Local Variable
        print("From Local Variable")
        print("Your Id is:",id)
        print("Your Name is:",name)

lc = local()
lc.globalexample()
lc.localexample()