import tkinter
from tkinter import ttk,messagebox

tk = tkinter.Tk()

tk.title("MyApp")
tk.config(bg='Lightblue')
tk.geometry("500x500")

# tkinter.Label(text="FirstName:").pack()

# tkinter.Label(text="FirstName:",bg="lightblue",fg="red",font="italic 15 bold").place(x=0,y=0)
# tkinter.Label(text="LastName:",bg="lightblue",fg="red",font="italic 15 bold").place(x=0,y=30)

tkinter.Label(text="FirstName:",bg="lightblue",fg="red",font="italic 15 bold").grid(row=0,column=0,sticky='w') # W means West side
tkinter.Label(text="LastName:",bg="lightblue",fg="red",font="italic 15 bold").grid(row=1,column=0,sticky='w')

tkinter.Entry().grid(row=0,column=1,sticky='w') # Entry Used for Taking User Input
tkinter.Entry().grid(row=1,column=1,sticky='w')

tkinter.Radiobutton(value=0,text='Male',bg="lightblue",fg="red",font="italic 15 bold").grid(row=2,column=0,sticky='w')
tkinter.Radiobutton(value=1,text='Female',bg="lightblue",fg="red",font="italic 15 bold").grid(row=2,column=1,sticky='w')

tkinter.Checkbutton(text="Gujarati",bg="lightblue",fg="red",font="italic 15 bold").grid(row=3,column=0,sticky='w')
tkinter.Checkbutton(text="Hindi",bg="lightblue",fg="red",font="italic 15 bold").grid(row=4,column=0,sticky='w')
tkinter.Checkbutton(text="English",bg="lightblue",fg="red",font="italic 15 bold").grid(row=5,column=0,sticky='w')

city = ['Rajkot','Ahmedabad','Baroda','Surat','Jamnagar']
ttk.Combobox(values=city).grid(row=6,column=0,sticky='w') # Combobox Used for Drop-Down Menu

def btnclick():
    print("This is Button!")
    # messagebox.showerror("Error!","Something Went Wrong...")
    # messagebox.showinfo("Success","Registration Succesfully!")
    messagebox.showwarning("Warning","Your Disk is full!")

tkinter.Button(text="Submit",fg="red",font="italic 15 bold",command=btnclick).grid(row=7,column=0)

tkinter.mainloop()