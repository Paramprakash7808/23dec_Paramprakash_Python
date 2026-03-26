import pymysql
import pandas

try:
    db = pymysql.connect(host='localhost',user='root',password='',database='studentdb')
    print("Database Created!")
except Exception as e:
    print(e)

cr = db.cursor()
# Table Create
tbl_create = 'create table student (id integer primary key auto_increment,name text,sub text)'
try:
    cr.execute(tbl_create)
    print("Table Created!")
except Exception as e:
    print(e)

# Insert Data
data_insert = 'insert into student (name,sub) values ("Prakash","Python"),("Meet","React")'
try:
    cr.execute(data_insert)
    db.commit()
    print("Data Inserted!")
except Exception as e:
    print(e)

# Update Data
update_data = "update student set name='Dhaval',sub='Flutter' where id = 2"
try:
    cr.execute(update_data)
    db.commit()
    print("Data Updated!")
except Exception as e:
    print(e)

# Delete Data
delete_data = "delete from student where id = 3"
try:
    cr.execute(delete_data)
    db.commit()
    print("Data Deleted!")
except Exception as e:
    print(e)

# # Display Data
# display_data = 'select * from student'
# try:
#     cr.execute(display_data)
#     data = cr.fetchall()
#     # data = cr.fetchmany(5)
#     # data = cr.fetchone()
#     # print(data)
#     for i in data:
#         print(i)
# except Exception as e:
#     print(e)

# Display Data Using Pandas Library To Print Data in Tabular Format
display_data = 'select * from student'
try:
    cr.execute(display_data)
    data = cr.fetchall()
    # data = cr.fetchmany(5)
    # data = cr.fetchone()
    # print(data)
    dt = pandas.DataFrame(data)
    print(dt)
except Exception as e:
    print(e)