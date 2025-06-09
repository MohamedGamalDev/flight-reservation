import tkinter as tk
from tkinter import ttk

from db import Database
from ui_add_flight import AddFlightUI
from ui_view_flights import ViewFlightsUI
from ui_reserve_seat import ReserveSeatUI
from ui_view_reservations import ViewReservationsUI

class FlightApp:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title(" Smart Flight Reservation System")
        self.root.geometry("800x700")
        self.root.configure(bg="#f4fbff")

        self.create_main_ui()

        # Instances of UI windows
        self.add_flight_ui = AddFlightUI(self.db)
        self.view_flights_ui = ViewFlightsUI(self.db)
        self.reserve_seat_ui = ReserveSeatUI(self.db)
        self.view_reservations_ui = ViewReservationsUI(self.db)

    def create_main_ui(self):
        title = tk.Label(self.root, text=" Smart Flight Reservation System", font=("Helvetica", 22, 'bold'), bg="#f4fbff", fg="#2c3e50")
        title.pack(pady=20)

        # Admin Panel
        admin_frame = tk.LabelFrame(self.root, text=" Admin Panel", bg="#e8f6ff", padx=10, pady=10, font=("Helvetica", 12, "bold"))
        admin_frame.pack(pady=15, padx=30, fill='x')

        ttk.Button(admin_frame, text=" Add Flight", width=40, command=lambda: self.add_flight_ui.open(self.root)).pack(pady=5)
        ttk.Button(admin_frame, text=" View Flights", width=40, command=lambda: self.view_flights_ui.open(self.root)).pack(pady=5)

        # Passenger Panel
        passenger_frame = tk.LabelFrame(self.root, text=" Passenger Panel", bg="#fdfefe", padx=10, pady=10, font=("Helvetica", 12, "bold"))
        passenger_frame.pack(pady=15, padx=30, fill='x')

        ttk.Button(passenger_frame, text=" Reserve Seat", width=40, command=lambda: self.reserve_seat_ui.open(self.root)).pack(pady=5)
        ttk.Button(passenger_frame, text=" View Reservations", width=40, command=lambda: self.view_reservations_ui.open(self.root)).pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = FlightApp(root)
    root.mainloop()
