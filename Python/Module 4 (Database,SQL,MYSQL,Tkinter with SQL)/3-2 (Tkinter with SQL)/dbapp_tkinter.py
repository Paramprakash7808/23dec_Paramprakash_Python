import tkinter
import sqlite3

tk = tkinter.Tk()
tk.title("Form")
tk.geometry("400x500")
tk.config(bg="lightblue")

lbl1 = tkinter.Label(text='Name:',bg='lightblue',fg='red',font='italic 15 bold')
lbl1.grid(row=0,column=0)

lbl2 = tkinter.Label(text='Subject:',bg='lightblue',fg='red',font='italic 15 bold')
lbl2.grid(row=1,column=0)

txt1 = tkinter.Entry()
txt1.grid(row=0,column=1)

txt2 = tkinter.Entry()
txt2.grid(row=1,column=1)

try:
    db = sqlite3.connect('tkdb.db')
    print("Database Connected!")
except Exception as e:
    print(e)

tbl_create = "create table collage (id integer primary key autoincrement,name text,sub text)"
try:
    db.execute(tbl_create)
    print("Table Created!")
except Exception as e:
    print(e)

def insertdata():
    name = txt1.get()
    sub = txt2.get()

    data_insert = f"insert into collage (name,sub) values ('{name}','{sub}')"
    try:
        db.execute(data_insert)
        db.commit()
        print("Data Inserted!")
    except Exception as e:
        print(e)

btn = tkinter.Button(text='Submit',fg='red',font="italic 15 bold",command=insertdata)
# btn.grid(row=2,column=0)
btn.place(x=100,y=80)

tk.mainloop()