num1 = int(input("Enter First Number: "))
num2 = int(input("Enter Second Number: "))

if num1 != 0 and num2 != 0:
    if num1>num2:
        print("Addition of First and Second Number is:",num1+num2)
    else:
        print("Multiplication of First and Second Number is:",num1*num2)
else:
    print("Invalid Number")

# age = int(input("Enter Your Age: "))

# if age>=18:
#     print("Eligible To Vote")
#     if age>=60:
#         print("Senior Citizen")
#     else:
#         print("Young Age")
# else:
#     print("Not Eligible To Vote")