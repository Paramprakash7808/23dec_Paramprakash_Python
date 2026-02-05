# Your task is to develop a Python-based console application, named MediTrack, that
# helps pharmacy staff handle medicine sales and maintain basic inventory control
# using only core Python features.

# Medicine Sale Entry
# • Allows staff to process a sale by:
# o Entering customer name, medicine
# name, and quantity purchased
# o Validating if enough stock is available
# o Recording sale date

# Inventory View & Update
# ● View current stock for all
# medicines
# ● Add new medicine entries or
# update stock quantity and
# price

from datetime import date

inventory = {
    "Paracetamol": [10, 50],
    "Aspirin": [8, 30]
}

def view_inventory():
    print("\nInventory List")
    for med in inventory:
        print("Medicine:", med)
        print("Price:", inventory[med][0])
        print("Stock:", inventory[med][1])
        print()

def add_or_update_medicine():
    name = input("Enter Medicine Name: ")

    try:
        price = int(input("Enter Price: "))
        stock = int(input("Enter Stock Quantity: "))
        inventory[name] = [price, stock]
        print("Medicine added or updated")
    except ValueError:
        print("Invalid input")

def process_sale():
    customer = input("Enter Customer Name: ")
    med_name = input("Enter Medicine Name: ")

    if med_name not in inventory:
        print("Medicine not available")
        return

    try:
        qty = int(input("Enter Quantity: "))
    except ValueError:
        print("Invalid quantity")
        return

    if qty > inventory[med_name][1]:
        print("Not enough stock")
        return

    total = qty * inventory[med_name][0]
    inventory[med_name][1] = inventory[med_name][1] - qty

    print("\nBill Details")
    print("Customer Name:", customer)
    print("Medicine Name:", med_name)
    print("Quantity:", qty)
    print("Total Amount:", total)
    print("Sale Date:", date.today())

while True:
    print("\n1. Medicine Sale")
    print("2. Add or Update Medicine")
    print("3. View Inventory")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        process_sale()
    elif choice == "2":
        add_or_update_medicine()
    elif choice == "3":
        view_inventory()
    elif choice == "4":
        print("Program closed")
        break
    else:
        print("Wrong choice")