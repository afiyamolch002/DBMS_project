import mysql.connector as mc
from tabulate import tabulate
import sys

# Welcome Message and Login
print("AIRPORT TICKET MANAGEMENT SYSTEM")
print("Login Info")
username = "ADMIN"
password = "FLIGHT123"
k = input("Username: ")

if k == username:
    a = input("Password: ")
    if a == password:
        print("WELCOME TO THE AIRPORT TICKET MANAGEMENT SYSTEM")

        # Function to insert data into Passenger_Info and Ticket_Info
        def insert():
            ch = 'y'
            while ch.lower() == 'y':
                try:
                    # Connect to the database
                    c = mc.connect(host='localhost', user='root', passwd='1729', database='flight_managment')
                    cr = c.cursor()

                    # Inserting into Passenger_Info table
                    print("Enter Data for Passenger_Info")
                    pno1 = input("Enter Passport Number: ")
                    pname = input("Enter Passenger Name: ")
                    dob = input("Enter Date of Birth (YYYY-MM-DD): ")
                    gender = input("Enter Gender: ")
                    nation = input("Enter Nationality: ")
                    dis = input("Enter Disability: ")
                    sql1 = "INSERT INTO passenger_info VALUES (%s, %s, %s, %s, %s, %s)"
                    cr.execute(sql1, (pno1, pname, dob, gender, nation, dis))
                    c.commit()

                    # Inserting into Ticket_Info table
                    print("Enter Data for Ticket_Info")
                    rno = int(input("Enter Reservation Number: "))
                    fno = int(input("Enter Flight Number: "))
                    destiny = input("Enter Destination: ")
                    doa = input("Enter Date Of Arrival (YYYY-MM-DD): ")
                    dod = input("Enter Date of Departure (YYYY-MM-DD): ")
                    rate = int(input("Enter Price of Ticket: "))
                    sql2 = "INSERT INTO ticket_info VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    cr.execute(sql2, (rno, fno, destiny, doa, dod, rate, pno1))
                    c.commit()

                    print("Data Inserted Successfully")
                except mc.Error as e:
                    print("Error:", e)
                    c.rollback()
                finally:
                    cr.close()
                    c.close()

                ch = input("Do you want to continue Inserting? (Y/N): ")

        # Function to display data from tables
        def display():
            ch = 'y'
            while ch.lower() == 'y':
                try:
                    c = mc.connect(host='localhost', user='root', passwd='1729', database='flight_managment')
                    cr = c.cursor()

                    print("Display Menu")
                    choice = int(input('''1. Passenger_Info
2. Ticket_Info
3. Passenger and Ticket Info (Join Query)
4. Number of Passengers (Group By)
Select table to display: '''))

                    if choice == 1:
                        cr.execute("SELECT * FROM passenger_info")
                        data = cr.fetchall()
                        print(tabulate(data, headers=['Passport_No', 'Passenger_Name', 'Date_of_birth', 'Gender', 'Nationality', 'Disability'], tablefmt='psql'))

                    elif choice == 2:
                        cr.execute("SELECT * FROM ticket_info")
                        data = cr.fetchall()
                        print(tabulate(data, headers=['Reservation_No', 'Flight_No', 'Destination', 'Date_Of_Arrival', 'Date_Of_Departure', 'Rate', 'Passport_No'], tablefmt='psql'))

                    elif choice == 3:
                        cr.execute("SELECT passenger_info.passport_no, passenger_name, nationality, reservation_no, flight_no, destination, rate "
                                   "FROM passenger_info "
                                   "JOIN ticket_info ON passenger_info.passport_no = ticket_info.passport_no")
                        data = cr.fetchall()
                        print(tabulate(data, headers=['Passport_No', 'Passenger_Name', 'Nationality', 'Reservation_No', 'Flight_No', 'Destination', 'Rate'], tablefmt='psql'))

                    elif choice == 4:
                        cr.execute("SELECT flight_no, destination, COUNT(*) AS no_of_passengers "
                                   "FROM ticket_info "
                                   "GROUP BY flight_no, destination")
                        data = cr.fetchall()
                        print(tabulate(data, headers=['Flight_No', 'Destination', 'No_of_passengers'], tablefmt='psql'))

                    else:
                        print("Invalid Input")
                except mc.Error as e:
                    print("Error:", e)
                finally:
                    cr.close()
                    c.close()

                ch = input("Do you want to continue displaying? (Y/N): ")

        # Function to delete data from tables
        def delete():
            ch = 'y'
            while ch.lower() == 'y':
                try:
                    c = mc.connect(host='localhost', user='root', passwd='1729', database='flight_managment')
                    cr = c.cursor()

                    choice = int(input('''1. Delete from Passenger_Info
2. Delete from Ticket_Info
Choose table to delete data: '''))

                    if choice == 1:
                        pno = input("Enter Passport Number to delete: ")
                        cr.execute("DELETE FROM passenger_info WHERE Passport_No = %s", (pno,))
                        c.commit()
                        print("Data deleted from Passenger_Info")

                    elif choice == 2:
                        rno = int(input("Enter Reservation Number to delete: "))
                        cr.execute("DELETE FROM ticket_info WHERE Reservation_No = %s", (rno,))
                        c.commit()
                        print("Data deleted from Ticket_Info")

                    else:
                        print("Invalid Input")
                except mc.Error as e:
                    print("Error:", e)
                    c.rollback()
                finally:
                    cr.close()
                    c.close()

                ch = input("Do you want to continue deleting? (Y/N): ")

        # Placeholder function for update
        def update():
            print("Update function is not yet implemented")

        # Placeholder function for search
        def search():
            print("Search function is not yet implemented")

        # Main loop for user choices
        ch1 = 'y'
        while ch1.lower() == 'y':
            ch2 = int(input('''1. Insert
2. Display
3. Delete
4. Update
5. Search
6. Quit
Enter your choice: '''))

            if ch2 == 1:
                insert()
            elif ch2 == 2:
                display()
            elif ch2 == 3:
                delete()
            elif ch2 == 4:
                update()
            elif ch2 == 5:
                search()
            elif ch2 == 6:
                print("Exiting the system.")
                sys.exit()
            else:
                print("Invalid Input")

            ch1 = input("Do you want to continue? (Y/N): ")

    else:
        print("Invalid Password")
else:
    print("Invalid Username")
