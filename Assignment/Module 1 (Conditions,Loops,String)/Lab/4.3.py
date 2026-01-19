# Practical Example 7: Write a Python program to calculate grades based on percentage using
# if-else ladder.

marks = float(input("Enter Your Marks: "))

if marks >= 90:
    print("A Grade")
elif marks >= 70:
    print("B Grade")
elif marks >= 55:
    print("C Grade")
elif marks >= 40:
    print("D Grade")
else:
    print("Fail")