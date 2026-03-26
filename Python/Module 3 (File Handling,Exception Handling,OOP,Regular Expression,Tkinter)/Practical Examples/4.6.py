# 6) Write a 
# Python program to check the current position of the file cursor using tell().

fi = open('temp.txt','r')
print("Initial Cursor Position:",fi.tell())

fi.read(5)
print("Cursor Position After Reading 5 Characters:",fi.tell())