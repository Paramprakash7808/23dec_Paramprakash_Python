import sqlite3

try:
    db = sqlite3.connect('newdb.db')
    print("Database Created!")
except Exception as e:
    print(e)

# table Create
create_data = "create table student (id integer primary key autoincrement,name text,sub text)"
try:
    db.execute(create_data)
    print("Table Created!")
except Exception as e:
    print(e)

# Insert Data
def insertdata():
    n = int(input("Enter Number Of Students:"))

    for i in range(n):
        name = input("Enter Your Name:")
        sub = input("Enter Your Subject:")

        data_insert = f"insert into student (name,sub) values ('{name}','{sub}')"
        try:
            db.execute(data_insert)
            db.commit()
            print("Data Inserted")
        except Exception as e:
            print(e)

# insertdata()

# Update Data
def updatedata():
    id = int(input("Enter Id Which You Want to Update:"))
    new_name = input("Enter New Name:")
    new_sub = input("Enter New Subject:")
    update_data = f"update student set name='{new_name}',sub='{new_sub}' where id = {id}"
    try:
        db.execute(update_data)
        db.commit()
        print("Data Updated")
    except Exception as e:
        print(e)

# updatedata()

# Delete Data
def deletedata():
    id = int(input("Enter Id Which You Want to Delete:"))
    delete_data = f"delete from student where id={id}"
    try:
        db.execute(delete_data)
        db.commit()
        print("Data Deleted")
    except Exception as e:
        print(e)

# deletedata()

# Display Data
def displaydata():
    cr = db.cursor()
    display_data = "select * from student"
    try:
        cr.execute(display_data)
        data = cr.fetchall()
        # print(data)
        for i in data:
            print(i)
    except Exception as e:
        print(e)

# displaydata()
while True:
    print("Enter 1 for Insert Data \nEnter 2 for Update Data \nEnter 3 for Delete Data \nEnter 4 for Display Data \nEnter 5 for Exit")
    choice = int(input("Enter Your Choice:"))

    if choice == 1:
        insertdata()
    elif choice == 2:
        updatedata()
    elif choice == 3:
        deletedata()
    elif choice == 4:
        displaydata()
    elif choice == 5:
        db.close()
        break
    else:
        print("Invalid Choice")