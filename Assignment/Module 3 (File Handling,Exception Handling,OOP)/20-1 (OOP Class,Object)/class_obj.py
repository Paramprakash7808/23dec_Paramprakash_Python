class data:
    stid = 101
    stname = 'Prakash'

    def getsum(self,a,b):
        print("Addition of A and B is:",a+b)

    def getdata(self,id,name):
        print("Your Id is:",id)
        print("Your Name is:",name)

dt = data()
dt.getsum(25,25)
dt.getdata(101,'Sahil')
print(dt.stid)
print(dt.stname)