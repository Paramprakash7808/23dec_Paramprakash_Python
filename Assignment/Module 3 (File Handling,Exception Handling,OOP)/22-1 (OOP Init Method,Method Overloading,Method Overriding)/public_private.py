class data:
    # Private Variable 
    __id = 101 # __ means Private
    __name = 'Prakash'

    # Private
    def __getdata(self):
        print("Your Id is:",self.__id)
        print("Your Name is:",self.__name)

    def printdata(self):
        self.__getdata()

dt = data()
# dt.__getdata() # We can't acces getdata method directly bacause getdata method is private
dt.printdata()