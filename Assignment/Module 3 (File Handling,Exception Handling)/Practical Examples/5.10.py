# 10) Write a Python program to print custom exceptions.

try:
    fi = open('data.txt','r')
    print(fi.read())
except:
    print("File Not Found")