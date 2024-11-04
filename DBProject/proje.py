import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector as mc

# Database credentials
db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '1729',
    'database': 'flight_managment'
}

# Initialize main application window
root = tk.Tk()
root.title("Airport Ticket Managment System")
root.geometry("600x600")
root.config(bg="white")

# Global variables for entry fields
username_var = tk.StringVar()
password_var = tk.StringVar()

# Frame for different pages
frames = {}

# Styles
header_font = ("Arial", 18, "bold")
label_font = ("Arial", 12)
entry_font = ("Arial", 12)

# Function to switch between frames
def show_frame(frame_name):
    frame = frames[frame_name]
    frame.tkraise()

# Function to handle login
def login():
    username = username_var.get()
    password = password_var.get()
    
    if username == "ADMIN" and password == "FLIGHT123":
        show_frame("Home")
        username_var.set("")
        password_var.set("")
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

# Database Operations
def execute_query(query, values=()):
    try:
        conn = mc.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        if query.strip().upper().startswith("SELECT"):
            return cursor.fetchall()
        return []
    except mc.Error as e:
        messagebox.showerror("Error", str(e))
        return []
    finally:
        cursor.close()
        conn.close()

# Check if a primary key exists
def primary_key_exists(query, values):
    results = execute_query(query, values)
    return len(results) > 0

# Insert Passenger Info
def insert_passenger():
    query = "INSERT INTO passenger_info VALUES (%s, %s, %s, %s, %s, %s)"
    values = (
        passport_no_var.get(), passenger_name_var.get(), dob_var.get(),
        gender_var.get(), nationality_var.get(), disability_var.get()
    )
    execute_query(query, values)
    messagebox.showinfo("Success", "Passenger data inserted successfully.")
    clear_passenger_entries()

# Display Passenger Info
def display_passenger():
    query = "SELECT * FROM passenger_info"
    results = execute_query(query)
    display_data(results, ["Passport_No", "Passenger_Name", "Date_of_Birth", "Gender", "Nationality", "Disability"])

# Delete Passenger Info
def delete_passenger():
    if not passport_no_var.get():
        messagebox.showerror("Error", "Please enter the Passport Number.")
        return
    
    query = "DELETE FROM passenger_info WHERE passport_no = %s"
    values = (passport_no_var.get(),)
    
    if primary_key_exists("SELECT * FROM passenger_info WHERE passport_no = %s", values):
        execute_query(query, values)
        messagebox.showinfo("Success", "Passenger data deleted successfully.")
    else:
        messagebox.showerror("Error", "Value is not present.")
    
    clear_passenger_entries()

# Update Passenger Info
def update_passenger():
    if not passport_no_var.get():
        messagebox.showerror("Error", "Please enter the Passport Number.")
        return
    
    if not primary_key_exists("SELECT * FROM passenger_info WHERE passport_no = %s", (passport_no_var.get(),)):
        messagebox.showerror("Error", "Value is not present.")
        return
    
    query = "UPDATE passenger_info SET passenger_name=%s, date_of_birth=%s, gender=%s, nationality=%s, disability=%s WHERE passport_no=%s"
    values = (
        passenger_name_var.get(), dob_var.get(), gender_var.get(),
        nationality_var.get(), disability_var.get(), passport_no_var.get()
    )
    execute_query(query, values)
    messagebox.showinfo("Success", "Passenger data updated successfully.")
    clear_passenger_entries()

# Search Passenger Info
def search_passenger():
    if not passport_no_var.get():
        messagebox.showerror("Error", "Please enter the Passport Number.")
        return
    
    values = (passport_no_var.get(),)
    if primary_key_exists("SELECT * FROM passenger_info WHERE passport_no = %s", values):
        query = "SELECT * FROM passenger_info WHERE passport_no = %s"
        results = execute_query(query, values)
        display_data(results, ["Passport_No", "Passenger_Name", "Date_of_Birth", "Gender", "Nationality", "Disability"])
    else:
        messagebox.showerror("Error", "Value is not present.")

# Clear Passenger Entry Fields
def clear_passenger_entries():
    passport_no_var.set("")
    passenger_name_var.set("")
    dob_var.set("")
    gender_var.set("")
    nationality_var.set("")
    disability_var.set("")

# Insert Ticket Info
def insert_ticket():
    query = "INSERT INTO ticket_info VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (
        reservation_no_var.get(), flight_no_var.get(), destination_var.get(),
        date_of_arrival_var.get(), date_of_departure_var.get(),
        rate_var.get(), ticket_passport_no_var.get()
    )
    execute_query(query, values)
    messagebox.showinfo("Success", "Ticket data inserted successfully.")
    clear_ticket_entries()

# Display Ticket Info
def display_ticket():
    query = "SELECT * FROM ticket_info"
    results = execute_query(query)
    display_data(results, ["Reservation_No", "Flight_No", "Destination", "Date_of_Arrival", "Date_of_Departure", "Rate", "Passport_No"])

# Delete Ticket Info
def delete_ticket():
    if not reservation_no_var.get():
        messagebox.showerror("Error", "Please enter the Reservation Number.")
        return
    
    query = "DELETE FROM ticket_info WHERE reservation_no = %s"
    values = (reservation_no_var.get(),)
    
    if primary_key_exists("SELECT * FROM ticket_info WHERE reservation_no = %s", values):
        execute_query(query, values)
        messagebox.showinfo("Success", "Ticket data deleted successfully.")
    else:
        messagebox.showerror("Error", "Value is not present.")
    
    clear_ticket_entries()

# Update Ticket Info
def update_ticket():
    if not reservation_no_var.get():
        messagebox.showerror("Error", "Please enter the Reservation Number.")
        return
    
    if not primary_key_exists("SELECT * FROM ticket_info WHERE reservation_no = %s", (reservation_no_var.get(),)):
        messagebox.showerror("Error", "Value is not present.")
        return
    
    query = "UPDATE ticket_info SET flight_no=%s, destination=%s, date_of_arrival=%s, date_of_departure=%s, rate=%s, passport_no=%s WHERE reservation_no=%s"
    values = (
        flight_no_var.get(), destination_var.get(), date_of_arrival_var.get(),
        date_of_departure_var.get(), rate_var.get(), ticket_passport_no_var.get(),
        reservation_no_var.get()
    )
    execute_query(query, values)
    messagebox.showinfo("Success", "Ticket data updated successfully.")
    clear_ticket_entries()

# Search Ticket Info
def search_ticket():
    if not reservation_no_var.get():
        messagebox.showerror("Error", "Please enter the Reservation Number.")
        return
    
    values = (reservation_no_var.get(),)
    if primary_key_exists("SELECT * FROM ticket_info WHERE reservation_no = %s", values):
        query = "SELECT * FROM ticket_info WHERE reservation_no = %s"
        results = execute_query(query, values)
        display_data(results, ["Reservation_No", "Flight_No", "Destination", "Date_of_Arrival", "Date_of_Departure", "Rate", "Passport_No"])
    else:
        messagebox.showerror("Error", "Value is not present.")

# Clear Ticket Entry Fields
def clear_ticket_entries():
    reservation_no_var.set("")
    flight_no_var.set("")
    destination_var.set("")
    date_of_arrival_var.set("")
    date_of_departure_var.set("")
    rate_var.set("")
    ticket_passport_no_var.set("")

# Display Data in a Popup Window
def display_data(data, headers):
    window = tk.Toplevel(root)
    window.title("Data Display")
    table = ttk.Treeview(window, columns=headers, show="headings")
    for header in headers:
        table.heading(header, text=header)
    for row in data:
        table.insert("", tk.END, values=row)
    table.pack(fill=tk.BOTH, expand=True)

# Home Page
home_frame = tk.Frame(root, bg="white")
frames["Home"] = home_frame
home_frame.grid(row=0, column=0, sticky="nsew")
tk.Label(home_frame, text="Welcome to the Airport Ticket Managment System", font=header_font, bg="white", fg="blue").pack(pady=20)
tk.Button(home_frame, text="Passenger Info", font=label_font, command=lambda: show_frame("PassengerInfo")).pack(pady=10)
tk.Button(home_frame, text="Ticket Info", font=label_font, command=lambda: show_frame("TicketInfo")).pack(pady=10)
          
tk.Button(home_frame, text="Logout", font=label_font, command=lambda: show_frame("Login")).pack(pady=10)

# Passenger Info Page
passenger_info_frame = tk.Frame(root, bg="white")
frames["PassengerInfo"] = passenger_info_frame
passenger_info_frame.grid(row=0, column=0, sticky="nsew")
passport_no_var, passenger_name_var, dob_var, gender_var, nationality_var, disability_var = (tk.StringVar() for _ in range(6))
tk.Label(passenger_info_frame, text="Passenger Information", font=header_font, bg="white", fg="blue").pack(pady=10)

fields = ["Passport Number", "Passenger Name", "Date of Birth (YYYY-MM-DD)", "Gender", "Nationality", "Disability"]
vars = [passport_no_var, passenger_name_var, dob_var, gender_var, nationality_var, disability_var]
for label_text, var in zip(fields, vars):
    tk.Label(passenger_info_frame, text=label_text + ":", font=label_font, bg="white").pack()
    tk.Entry(passenger_info_frame, textvariable=var, font=entry_font).pack()

# Add buttons for Passenger Info operations
for text, command in [("Insert", insert_passenger), ("Update", update_passenger), ("Delete", delete_passenger), ("Search", search_passenger), ("Display", display_passenger)]:
    tk.Button(passenger_info_frame, text=text, font=label_font, command=command).pack(pady=2)
tk.Button(passenger_info_frame, text="Back to Home", font=label_font, command=lambda: show_frame("Home")).pack()

# Ticket Info Page
ticket_info_frame = tk.Frame(root, bg="white")
frames["TicketInfo"] = ticket_info_frame
ticket_info_frame.grid(row=0, column=0, sticky="nsew")
reservation_no_var, flight_no_var, destination_var, date_of_arrival_var, date_of_departure_var, rate_var, ticket_passport_no_var = (tk.StringVar() for _ in range(7))
tk.Label(ticket_info_frame, text="Ticket Information", font=header_font, bg="white", fg="blue").pack(pady=10)

fields = ["Reservation Number", "Flight Number", "Destination", "Date of Arrival (YYYY-MM-DD)", "Date of Departure (YYYY-MM-DD)", "Rate", "Passport Number"]
vars = [reservation_no_var, flight_no_var, destination_var, date_of_arrival_var, date_of_departure_var, rate_var, ticket_passport_no_var]
for label_text, var in zip(fields, vars):
    tk.Label(ticket_info_frame, text=label_text + ":", font=label_font, bg="white").pack()
    tk.Entry(ticket_info_frame, textvariable=var, font=entry_font).pack()

# Add buttons for Ticket Info operations
for text, command in [("Insert", insert_ticket), ("Update", update_ticket), ("Delete", delete_ticket), ("Search", search_ticket), ("Display", display_ticket)]:
    tk.Button(ticket_info_frame, text=text, font=label_font, command=command).pack(pady=2)
tk.Button(ticket_info_frame, text="Back to Home", font=label_font, command=lambda: show_frame("Home")).pack()

# Login Page
login_frame = tk.Frame(root, bg="white")
frames["Login"] = login_frame
login_frame.grid(row=0, column=0, sticky="nsew")
tk.Label(login_frame, text="Login", font=header_font, bg="white", fg="blue").pack(pady=20)
tk.Label(login_frame, text="Username:", font=label_font, bg="white").pack()
tk.Entry(login_frame, textvariable=username_var, font=entry_font).pack()
tk.Label(login_frame, text="Password:", font=label_font, bg="white").pack()
tk.Entry(login_frame, textvariable=password_var, show="*", font=entry_font).pack()
tk.Button(login_frame, text="Login", font=label_font, command=login).pack(pady=10)

# Start on the Login Page
show_frame("Login")



# Run the application
root.mainloop()

