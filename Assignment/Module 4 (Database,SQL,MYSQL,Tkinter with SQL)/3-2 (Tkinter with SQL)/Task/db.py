import sqlite3

try:
    db = sqlite3.connect("newdb.db")
    print("Database Connected!")
except Exception as e:
    print(e)

tbl_create = "create table student(id integer primary key autoincrement,name text,sub text)"
try:
    db.execute(tbl_create)
    print("Table Created!")
except Exception as e:
    print(e)


def insertdata():
    n = int(input("Enter Number of Students:"))

    for i in range(n):
        name = input("Enter Your Name:")
        sub = input("Enter Your Subject:")

        insert_q = f"insert into student(name,sub) values ('{name}','{sub}')"
        try:
            db.execute(insert_q)
            db.commit()
            print("Data Inserted!")
        except Exception as e:
            print(e)

def updatedata():
    n = int(input("Enter Id:"))

    name = input("Enter Your Name:")
    sub = input("Enter Your Subject:")

    update_q = f"Update student set name:{name},subject:{sub} where id:{n})"
    try:
        db.execute(update_q)
        db.commit()
        print("Data Updated!")
    except Exception as e:
        print(e)

def deletedata():
    n = int(input("Enter Id:"))

    delete_q = f"delete from student where id:{n}"
    try:
        db.execute(delete_q)
        db.commit()
        print("Data Deleted!")
    except Exception as e:
        print(e)

def Displaydata():
    try:
        cursor = db.execute("Select * from student")
        data = cursor.fetchall()
        db.commit()
        for i in data:
            print(i)
        print("Data Deleted!")
    except Exception as e:
        print(e)

while True:
    print("Enter 1 for Insert Data \n Enter 2 for Update Data \n Enter 3 for Delete Data \n Enter 4 for Display Data")
    choice = int(input("Enter Your Choice:"))

    if choice == 1:
        insertdata()
    elif choice == 2:
        updatedata()
    elif choice == 3:
        deletedata()
    elif choice == 4:
        Displaydata()
    else:
        print("Invalid Choice!")