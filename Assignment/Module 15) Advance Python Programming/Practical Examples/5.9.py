# 9) Write a Python program to handle file exceptions and use the finally block for closing 
# the file.

try:
    fi = open('data.txt','r')
    print(fi.read())
except FileNotFoundError:
    print("File Not Found")
finally:
    try:
        fi.close()
        print("File Closed Succesfully")
    except NameError:
        pass