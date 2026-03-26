# 22) Write a Python program to insert data into an SQLite3 database and fetch it.

import sqlite3

try:
    db = sqlite3.connect('newdata.db')
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

# Insert Data
insert_data = "insert into student (name,sub) values ('Prakash','Python'),('Meet','React')"
try:
    db.execute(insert_data)
    db.commit()
    print("Data Inserted!")
except Exception as e:
    print(e)

# Display Data
cr = db.cursor()
display_data = "select * from student"
try:
    cr.execute(display_data)
    data = cr.fetchall()
    # data = cr.fetchmany(5)
    # data = cr.fetchone()

    for i in data:
        print(i)
except Exception as e:
    print(e)