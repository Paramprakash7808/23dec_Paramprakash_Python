# Practical Example 8: Write a Python program to check if a person is eligible to donate blood
# using a nested if.

age = int(input("Enter Your Age: "))
blood = input("Enter Your Blood Group: ")

if age >= 18:
    if blood == "A+":
        print("You Are Eligible to Donate Blood")
    elif blood == "A-":
        print("You Are Eligible to Donate Blood")
    elif blood == "B+":
        print("You Are Eligible to Donate Blood")
    elif blood == "B-":
        print("You Are Eligible to Donate Blood")
    elif blood == "O+":
        print("You Are Eligible to Donate Blood")
    elif blood == "O-":
        print("You Are Eligible to Donate Blood")
    else:
        print("Invalid Blood Group")
else:
    print("You Are Not Eligible Because Your Age is below 18")