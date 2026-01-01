fullname = input("Enter Your FullName: ")
if fullname.isalpha():
    print("Your Name: ",fullname)

    email = input("Enter Your Email: ")
    if email.islower():
        print("Your Email is: ",email)

        password = input("Enter Your Password: ")
        confirm_password = input("Retype Password: ")
        if len(password) >= 8 and len(password) <= 12:
            if password == confirm_password:
                print("Your Password is: ",password)

                number = input("Enter Your Mobile Number: ")
                if len(number) == 10:
                    print("Your Number is: ",number)
                else:
                    print("Enter Valid Mobile Number")
            else:
                print("Password Not Matched")
        else:
            print("Enter Password in Range From 8 to 12 Characters")
    else:
        print("Enter Valid Email")
else:
    print("Enter Valid FullName")