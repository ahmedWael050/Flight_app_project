Flight Reservation System

A simple desktop application built with Python, Tkinter, and SQLite that allows users to manage flights and reservations.

# Features
🔹 Flight Management

Add new flights with details such as flight number, origin, destination, date, time, and price.

View all available flights in a clean table view.

Edit flight details.

Delete flights.

Refresh flight list dynamically.

# Reservation Management

Reserve a flight for a passenger by entering their name and flight number.

View all reservations in a separate window.

Edit existing reservations (update passenger name or flight number).

Delete reservations.

Refresh reservations dynamically.

# User Interface

Built with Tkinter for a clean and modern GUI.

Styled using ttk themes for better readability.

Organized into different frames: flight management, available flights, reservations.

# Database

Uses SQLite (flights.db) to store flights and reservations.

Automatic table creation if the database doesn’t exist.

# Deployment

Application can be converted into a standalone executable (.exe) using PyInstaller, making it easy to run without requiring Python installation.

# Tech Stack

Python 3

Tkinter (GUI)

SQLite (Database)

ttk (Styling and Treeview)

PyInstaller (for creating .exe file)
# Running Options 💻

Option 1: Run the Python file:
flight_app3.py


Option 2: Use the prebuilt .exe:
If you don’t have Python installed, you can run the included flight_app3.exe file directly from the repository.


Option 3: Clone the repository:

git clone <https://github.com/ahmedWael050/flight_app_project.git>
cd flight_app_project


Install Python (if not already installed).

Run the program:

flight_app3.py


(Optional) Convert to .exe using PyInstaller:

pyinstaller --onefile --windowed main.py


The .exe file will be available inside the dist/ folder.

-Notes

The app is a learning project built during the Sprints × Microsoft Summer Camp – Programming using Python.
Focus is on understanding Python fundamentals, OOP, databases, and GUI development.

It’s a step towards building larger, more feature-rich applications.
