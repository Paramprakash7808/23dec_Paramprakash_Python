# Practical Example 4: Print this pattern using nested for loop:
# *
# **
# ***
# ****
# *****

for i in range(1,6):
    for j in range(i):
        print("*",end=" ")
    print(" ")