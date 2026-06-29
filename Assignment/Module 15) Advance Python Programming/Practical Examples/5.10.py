# 10) Write a Python program to print custom exceptions.

try:
    fi = open('data.txt','r')
    print(fi.read())
    fi.close()
except:
    print("File Not Found")