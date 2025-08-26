import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Database Setup
conn = sqlite3.connect("flights.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS flights (
    flight_no TEXT PRIMARY KEY,
    origin TEXT,
    destination TEXT,
    date TEXT,
    time TEXT,
    price REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    passenger_name TEXT,
    flight_no TEXT,
    FOREIGN KEY(flight_no) REFERENCES flights(flight_no)
)
""")

conn.commit()

# Functions
def add_flight():
    try:
        cursor.execute("INSERT INTO flights VALUES (?, ?, ?, ?, ?, ?)", (
            flight_no_entry.get(), origin_entry.get(), dest_entry.get(), date_entry.get(),
            time_entry.get(), float(price_entry.get())
        ))
        conn.commit()
        messagebox.showinfo("Success", "Flight added successfully!")
        view_flights()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def view_flights():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM flights")
    for flight in cursor.fetchall():
        tree.insert("", tk.END, values=flight)

def reserve_flight():
    passenger = passenger_entry.get()
    flight_no = flight_no_reserve_entry.get()
    cursor.execute("SELECT * FROM flights WHERE flight_no=?", (flight_no,))
    if cursor.fetchone():
        cursor.execute("INSERT INTO reservations (passenger_name, flight_no) VALUES (?, ?)", (passenger, flight_no))
        conn.commit()
        messagebox.showinfo("Success", f"Reservation completed for {passenger} on flight {flight_no}!")
    else:
        messagebox.showerror("Error", "Flight not found!")

def view_reservations():
    res_win = tk.Toplevel(root)
    res_win.title("Reservations")
    res_win.configure(bg="#f4f6f9")
    res_win.geometry("600x400")

    tree_res = ttk.Treeview(res_win, columns=("ID", "Passenger", "Flight"), show="headings", height=10)
    style = ttk.Style()
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

    for col in ("ID", "Passenger", "Flight"):
        tree_res.heading(col, text=col)
        tree_res.column(col, anchor="center", width=150)
    tree_res.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def refresh_res():
        for row in tree_res.get_children():
            tree_res.delete(row)
        cursor.execute("SELECT * FROM reservations")
        for res in cursor.fetchall():
            tree_res.insert("", tk.END, values=res)

    def delete_reservation():
        selected = tree_res.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a reservation to delete.")
            return
        res_id = tree_res.item(selected[0])['values'][0]
        cursor.execute("DELETE FROM reservations WHERE id=?", (res_id,))
        conn.commit()
        refresh_res()
        messagebox.showinfo("Deleted", "Reservation deleted successfully!")

    def edit_reservation():
        selected = tree_res.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a reservation to edit.")
            return
        res_id, passenger_name, flight_no = tree_res.item(selected[0])['values']

        edit_win = tk.Toplevel(res_win)
        edit_win.title("Edit Reservation")
        tk.Label(edit_win, text="Passenger Name").grid(row=0, column=0, padx=5, pady=5)
        new_name = tk.Entry(edit_win)
        new_name.insert(0, passenger_name)
        new_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(edit_win, text="Flight No").grid(row=1, column=0, padx=5, pady=5)
        new_flight = tk.Entry(edit_win)
        new_flight.insert(0, flight_no)
        new_flight.grid(row=1, column=1, padx=5, pady=5)

        def save_edit():
            cursor.execute("UPDATE reservations SET passenger_name=?, flight_no=? WHERE id=?",
                           (new_name.get(), new_flight.get(), res_id))
            conn.commit()
            refresh_res()
            edit_win.destroy()
            messagebox.showinfo("Updated", "Reservation updated successfully!")

        ttk.Button(edit_win, text="Save", command=save_edit).grid(row=2, column=0, columnspan=2, pady=10)

    ttk.Button(res_win, text="Refresh", command=refresh_res).pack(side="left", padx=10, pady=5)
    ttk.Button(res_win, text="Edit", command=edit_reservation).pack(side="left", padx=10, pady=5)
    ttk.Button(res_win, text="Delete", command=delete_reservation).pack(side="left", padx=10, pady=5)

    refresh_res()

def delete_flight():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "Please select a flight to delete.")
        return
    flight_no = tree.item(selected[0])['values'][0]
    cursor.execute("DELETE FROM flights WHERE flight_no=?", (flight_no,))
    conn.commit()
    view_flights()
    messagebox.showinfo("Deleted", "Flight deleted successfully!")

def edit_flight():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "Please select a flight to edit.")
        return
    flight = tree.item(selected[0])['values']

    edit_win = tk.Toplevel(root)
    edit_win.title("Edit Flight")

    labels = ["Flight No", "Origin", "Destination", "Date", "Time", "Price"]
    entries = []
    for i, label in enumerate(labels):
        tk.Label(edit_win, text=label).grid(row=i, column=0, padx=5, pady=5)
        e = tk.Entry(edit_win)
        e.insert(0, flight[i])
        e.grid(row=i, column=1, padx=5, pady=5)
        entries.append(e)

    def save_edit():
        cursor.execute("""UPDATE flights SET origin=?, destination=?, date=?, time=?, price=?
                          WHERE flight_no=?""",
                       (entries[1].get(), entries[2].get(), entries[3].get(),
                        entries[4].get(), float(entries[5].get()), entries[0].get()))
        conn.commit()
        view_flights()
        edit_win.destroy()
        messagebox.showinfo("Updated", "Flight updated successfully!")

    ttk.Button(edit_win, text="Save", command=save_edit).grid(row=len(labels), column=0, columnspan=2, pady=10)

# GUI Setup
root = tk.Tk()
root.title("✈ Flight Reservation System")
root.geometry("1000x600")
root.configure(bg="#f4f6f9")

# General Style
style = ttk.Style()
style.theme_use("clam")

style.configure("TButton", font=("Segoe UI", 11, "bold"), background="#0066cc", foreground="white", padding=8, relief="flat")
style.map("TButton", background=[("active", "#004d99")])

style.configure("Treeview", font=("Segoe UI", 10), rowheight=28, background="white", fieldbackground="white")
style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#0066cc", foreground="white")

style.configure("TLabel", font=("Segoe UI", 10), background="#f0f2f5")

# Add Flight Frame
frame1 = tk.LabelFrame(root, text="Add Flight", font=("Segoe UI", 12, "bold"), bg="#f4f6f9", fg="#333")
frame1.pack(fill="x", padx=15, pady=10)

labels = ["Flight No", "Origin", "Destination", "Date", "Time", "Price"]
entries = []
for i, label in enumerate(labels):
    tk.Label(frame1, text=label, font=("Segoe UI", 10, "bold"), bg="#f4f6f9").grid(row=0, column=i, padx=5, pady=5)

flight_no_entry = tk.Entry(frame1)
origin_entry = tk.Entry(frame1)
dest_entry = tk.Entry(frame1)
date_entry = tk.Entry(frame1)
time_entry = tk.Entry(frame1)
price_entry = tk.Entry(frame1)

entries = [flight_no_entry, origin_entry, dest_entry, date_entry, time_entry, price_entry]
for i, entry in enumerate(entries):
    entry.grid(row=1, column=i, padx=5, pady=5)

ttk.Button(frame1, text="Add Flight", command=add_flight).grid(row=1, column=len(entries), padx=10)

# View Flights Frame
frame2 = tk.LabelFrame(root, text="Available Flights", font=("Segoe UI", 12, "bold"), bg="#f4f6f9", fg="#333")
frame2.pack(fill="both", padx=15, pady=10, expand=True)

tree = ttk.Treeview(frame2, columns=labels, show="headings", height=10)
for col in labels:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=120)
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

btn_frame = tk.Frame(frame2, bg="#f4f6f9")
btn_frame.pack(pady=5)
ttk.Button(btn_frame, text="Refresh Flights", command=view_flights).pack(side="left", padx=5)
ttk.Button(btn_frame, text="Edit Flight", command=edit_flight).pack(side="left", padx=5)
ttk.Button(btn_frame, text="Delete Flight", command=delete_flight).pack(side="left", padx=5)

# Reservation Frame
frame3 = tk.LabelFrame(root, text="Reserve Flight", font=("Segoe UI", 12, "bold"), bg="#f4f6f9", fg="#333")
frame3.pack(fill="x", padx=15, pady=10)

tk.Label(frame3, text="Passenger Name", font=("Segoe UI", 10, "bold"), bg="#f4f6f9").grid(row=0, column=0, padx=5, pady=5)
passenger_entry = tk.Entry(frame3)
passenger_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame3, text="Flight No", font=("Segoe UI", 10, "bold"), bg="#f4f6f9").grid(row=0, column=2, padx=5, pady=5)
flight_no_reserve_entry = tk.Entry(frame3)
flight_no_reserve_entry.grid(row=0, column=3, padx=5, pady=5)

ttk.Button(frame3, text="Reserve", command=reserve_flight).grid(row=0, column=4, padx=10)

# View Reservations Button
ttk.Button(root, text="View Reservations", command=view_reservations).pack(pady=15)

root.mainloop()
