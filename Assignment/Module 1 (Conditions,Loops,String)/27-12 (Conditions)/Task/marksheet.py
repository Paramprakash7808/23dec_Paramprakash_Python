Gujarati = int(input("Enter Marks For Gujarati: "))
Hindi = int(input("Enter Marks For Hindi: "))
English = int(input("Enter Marks For English: "))
Science = int(input("Enter Marks For Science: "))

if Gujarati>=40 and Hindi>=40 and English>=40 and Science>=40:

    total = Gujarati + Hindi + English + Science
    print("Total Marks are:", total)

    per = total/4
    print("Percentage is:",per)

    if per>=70:
        print("A+ Grade")
    elif per>=60:
        print("A Grade")
    elif per>=50:
        print("B Grade")
    elif per>=40:
        print("C Grade")
else:
    print("Fail")