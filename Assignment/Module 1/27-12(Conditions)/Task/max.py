num1 = int(input("Enter First Number: "))
num2 = int(input("Enter Second Number: "))
num3 = int(input("Enter Third Number: "))

if num1>num2 and num1>num3:
    print("First Number is Maximum")
elif num2>num3 and num2>num1:
    print("Second Number is Maximum")
elif num3>num1 and num3>num2:
    print("Third Number is Maximum")
else:
    print("Inavalid Number")