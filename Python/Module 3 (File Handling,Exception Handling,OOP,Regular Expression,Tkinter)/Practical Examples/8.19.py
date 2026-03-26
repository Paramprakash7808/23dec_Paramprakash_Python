# 19) Write a Python program to show method overloading.

class data:
    # Method Overloading
    def getdata(self,id):
        print("Your Id is:",id)

    def getdata(self,name):
        print("Your Name is:",name)

dt = data()
dt.getdata("Prakash")