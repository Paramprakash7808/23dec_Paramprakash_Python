class data:
    id = 101
    name = 'Prakash'

    def printdata(self):
        print("This is Class's Function")

dt = data() #Object of Class
print("Your Id is:",dt.id)
print("Your Name is:",dt.name)
dt.printdata()