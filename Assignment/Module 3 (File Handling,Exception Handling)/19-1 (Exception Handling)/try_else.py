try: # If Try block Executed Succesfully Then Else Will be Printed and If Try blocks failed Then Except Printed 
    no1 = int(input("Enter Value of No1:"))
    no2 = int(input("Enter Value of No2:"))
    print("Addition of No1 and No2 is:",no1+no2)
except:
    print("Error!")
else:
    print("Else Example")