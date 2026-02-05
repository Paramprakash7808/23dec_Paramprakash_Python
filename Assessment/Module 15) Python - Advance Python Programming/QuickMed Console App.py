# You are working as an Advanced Python Developer at a software development firm.
# One of your clients, TechRepair Hub, is a large electronics repair chain that wants to
# digitize their operations. They’ve requested a Python-based desktop application
# called RepairMate that can streamline customer information, repair tracking, billing,
# and user access — all from a simple GUI.
# This application will involve file operations, exception handling, object-oriented
# programming, basic database connectivity, and a Tkinter-based GUI.

import tkinter as tk
from tkinter import messagebox
import sqlite3
import re
from datetime import date

# ---------------- DATABASE ----------------
conn = sqlite3.connect("repairmate.db")
cur = conn.cursor()

# Customer Table
cur.execute("""
CREATE TABLE IF NOT EXISTS customers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
""")

# Device Table (Multiple devices per customer)
cur.execute("""
CREATE TABLE IF NOT EXISTS devices(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    device_name TEXT
)
""")

# Repairs Table
cur.execute("""
CREATE TABLE IF NOT EXISTS repairs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    device_id INTEGER,
    issue TEXT,
    technician TEXT,
    status TEXT,
    service REAL,
    parts REAL,
    tax REAL,
    total REAL,
    repair_date TEXT
)
""")

conn.commit()

# ---------------- OOP ----------------
class Person:
    def __init__(self, name):
        self.name = name

    def role(self):
        return "User"

class Technician(Person):
    def role(self):
        return "Technician"

class Admin(Person):
    def role(self):
        return "Admin"

# ---------------- FILE HANDLING ----------------
def save_invoice(customer, device, total):
    with open("invoice.txt", "a") as f:
        f.write(f"{date.today()} | {customer} | {device} | {total}\n")

def read_invoice():
    try:
        with open("invoice.txt", "r") as f:
            return f.read()
    except:
        return "No invoices found"

# ---------------- LOGIN ----------------
current_user = None

def login():
    global current_user
    name = user_entry.get()
    role = role_var.get()

    if name == "":
        messagebox.showerror("Error", "Enter username")
        return

    if role == "Admin":
        current_user = Admin(name)
    else:
        current_user = Technician(name)

    messagebox.showinfo("Login", f"{current_user.role()} logged in")

# ---------------- CUSTOMER & DEVICE ----------------
def add_customer_device():
    try:
        cname = cust_entry.get()
        dname = device_entry.get()

        if cname == "" or dname == "":
            raise ValueError

        # Insert customer
        cur.execute("INSERT OR IGNORE INTO customers(name) VALUES(?)", (cname,))
        conn.commit()

        cur.execute("SELECT id FROM customers WHERE name=?", (cname,))
        cid = cur.fetchone()[0]

        # Insert device
        cur.execute("INSERT INTO devices(customer_id, device_name) VALUES(?,?)",
                    (cid, dname))
        conn.commit()

        messagebox.showinfo("Success", "Customer & Device Added")

    except:
        messagebox.showerror("Error", "Invalid input")

# ---------------- REPAIR ENTRY ----------------
def add_repair():
    try:
        if current_user is None:
            raise PermissionError

        cname = cust_entry.get()
        dname = device_entry.get()
        issue = issue_entry.get()
        tech = tech_entry.get()

        service = float(service_entry.get())
        parts = float(parts_entry.get())

        tax = (service + parts) * 0.10
        total = service + parts + tax

        # Get IDs
        cur.execute("SELECT id FROM customers WHERE name=?", (cname,))
        cid = cur.fetchone()[0]

        cur.execute("""
        SELECT id FROM devices 
        WHERE device_name=? AND customer_id=?
        """, (dname, cid))
        did = cur.fetchone()[0]

        cur.execute("""
        INSERT INTO repairs
        (customer_id, device_id, issue, technician, status,
         service, parts, tax, total, repair_date)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (cid, did, issue, tech, "Pending",
              service, parts, tax, total, date.today()))

        conn.commit()
        save_invoice(cname, dname, total)

        messagebox.showinfo("Success", "Repair Added")

    except PermissionError:
        messagebox.showerror("Error", "Login required")
    except:
        messagebox.showerror("Error", "Check Customer/Device")

# ---------------- UPDATE STATUS ----------------
def update_status():
    try:
        if current_user.role() != "Admin":
            raise PermissionError

        rid = int(status_id_entry.get())
        new_status = status_entry.get()

        cur.execute("UPDATE repairs SET status=? WHERE id=?",
                    (new_status, rid))
        conn.commit()

        messagebox.showinfo("Updated", "Status Updated")

    except PermissionError:
        messagebox.showerror("Denied", "Admin only")
    except:
        messagebox.showerror("Error", "Invalid Data")

# ---------------- HISTORY ----------------
def view_history():
    result_box.delete(0, tk.END)

    cur.execute("""
    SELECT customers.name, devices.device_name,
           repairs.issue, repairs.status, repairs.total
    FROM repairs
    JOIN customers ON repairs.customer_id = customers.id
    JOIN devices ON repairs.device_id = devices.id
    """)

    for row in cur.fetchall():
        result_box.insert(tk.END, row)

# ---------------- REGEX SEARCH ----------------
def search_repairs():
    pattern = search_entry.get()
    result_box.delete(0, tk.END)

    cur.execute("""
    SELECT customers.name, devices.device_name,
           repairs.issue, repairs.status
    FROM repairs
    JOIN customers ON repairs.customer_id = customers.id
    JOIN devices ON repairs.device_id = devices.id
    """)

    for row in cur.fetchall():
        if re.search(pattern, str(row), re.IGNORECASE):
            result_box.insert(tk.END, row)

# ---------------- SHOW INVOICE ----------------
def show_invoice():
    messagebox.showinfo("Invoices", read_invoice())

# ---------------- GUI ----------------
root = tk.Tk()
root.title("RepairMate")

# Login
tk.Label(root, text="Username").grid(row=0, column=0)
user_entry = tk.Entry(root)
user_entry.grid(row=0, column=1)

tk.Label(root, text="Role").grid(row=0, column=2)
role_var = tk.StringVar(value="Technician")
tk.Entry(root, textvariable=role_var).grid(row=0, column=3)

tk.Button(root, text="Login", command=login).grid(row=0, column=4)

# Customer + Device
tk.Label(root, text="Customer").grid(row=1, column=0)
cust_entry = tk.Entry(root)
cust_entry.grid(row=1, column=1)

tk.Label(root, text="Device").grid(row=1, column=2)
device_entry = tk.Entry(root)
device_entry.grid(row=1, column=3)

tk.Button(root, text="Add Customer & Device",
          command=add_customer_device).grid(row=1, column=4)

# Repair
tk.Label(root, text="Issue").grid(row=2, column=0)
issue_entry = tk.Entry(root)
issue_entry.grid(row=2, column=1)

tk.Label(root, text="Technician").grid(row=2, column=2)
tech_entry = tk.Entry(root)
tech_entry.grid(row=2, column=3)

tk.Label(root, text="Service Cost").grid(row=3, column=0)
service_entry = tk.Entry(root)
service_entry.grid(row=3, column=1)

tk.Label(root, text="Parts Cost").grid(row=3, column=2)
parts_entry = tk.Entry(root)
parts_entry.grid(row=3, column=3)

tk.Button(root, text="Add Repair", command=add_repair).grid(row=3, column=4)

# Status Update
tk.Label(root, text="Repair ID").grid(row=4, column=0)
status_id_entry = tk.Entry(root)
status_id_entry.grid(row=4, column=1)

tk.Label(root, text="New Status").grid(row=4, column=2)
status_entry = tk.Entry(root)
status_entry.grid(row=4, column=3)

tk.Button(root, text="Update Status", command=update_status).grid(row=4, column=4)

# Search + History
tk.Label(root, text="Search").grid(row=5, column=0)
search_entry = tk.Entry(root)
search_entry.grid(row=5, column=1)

tk.Button(root, text="Search", command=search_repairs).grid(row=5, column=2)
tk.Button(root, text="View History", command=view_history).grid(row=5, column=3)
tk.Button(root, text="View Invoice", command=show_invoice).grid(row=5, column=4)

result_box = tk.Listbox(root, width=130)
result_box.grid(row=6, column=0, columnspan=5)

root.mainloop()