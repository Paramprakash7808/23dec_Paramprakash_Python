# class bank
# -name
# -ac number(Random)
# -ac bal

# class deposit
# -amont>2000

# class withdraw
# -amont>2000 not then inefficient bal

# class statement
# -name
# -no
# -bal


import random

class bank:
    def data(self):
        self.acc_name = input("Enter Your Name:")
        self.acc_no = random.randint(100000,900000)
        self.acc_bal = 0

class deposit(bank):
    def dep(self):
        amt = int(input("Enter Amount:"))
        if amt > 0:
            self.acc_bal += amt
            print(f"Deposited Amount: {amt}")
            # print(f"New Balance: {self.acc_bal}")
        else:
            print("Invalid Amount")

class withdraw(deposit):
    def wit(self):
        amt = int(input("Enter Amount For Withdraw:"))

        min_bal = 2000
        with_limit = self.acc_bal - amt

        if amt <= 0:
            print("insufficient Balance")
        elif with_limit <= min_bal:
            print("Minimum Balance Must be 2000")
        else:
            self.acc_bal -= amt
            print(f"Withdrawen: {amt}")
            print(f"Remaining Balance: {self.acc_bal}")

class statement(withdraw):
    def stmt(self):
        print("Your Name is:",self.acc_name)
        print("Your Account Number:",self.acc_no)
        print("Your Current Balance is:",self.acc_bal)

st = statement()
st.data()
st.dep()
st.wit()
st.stmt()