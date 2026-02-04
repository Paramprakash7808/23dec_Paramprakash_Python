# 21) Write a Python program to create a database and a table using 
# SQLite3.

import sqlite3

try:
    db = sqlite3.connect('data.db')
    print("Database Connected!")
except Exception as e:
    print(e)

# Table Create
tbl_create = 'create table student(id integer primary key autoincrement,name text,sub text)'
try:
    db.execute(tbl_create)
    print("Table Created!")
except Exception as e:
    print(e)