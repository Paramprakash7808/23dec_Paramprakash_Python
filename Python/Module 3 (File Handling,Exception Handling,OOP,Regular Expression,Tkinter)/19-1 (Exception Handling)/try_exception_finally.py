try:
    no1 = int(input("Enter Value of No1:"))
    no2 = int(input("Enter Value of No2:"))
    print("Addition of No1 and No2 is:",no1+no2)
except:
    print("Error!")
finally:
    print("Finally Block Always Executed")