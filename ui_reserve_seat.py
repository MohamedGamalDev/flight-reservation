import tkinter as tk
from tkinter import ttk, messagebox

class ReserveSeatUI:
    def __init__(self, db):
        self.db = db

    def open(self, parent):
        self.win = tk.Toplevel(parent)
        self.win.title("🛫 Reserve a Seat")
        self.win.geometry("500x450")
        self.win.configure(bg="#f0faff")

        tk.Label(self.win, text=" Passenger Name (First Middle Last):", bg="#f0faff").pack(pady=2)
        self.name_entry = tk.Entry(self.win)
        self.name_entry.pack()

        tk.Label(self.win, text=" ID Number (14 digits):", bg="#f0faff").pack(pady=2)
        self.id_entry = tk.Entry(self.win)
        self.id_entry.pack()

        tk.Label(self.win, text=" Phone Number (11 digits):", bg="#f0faff").pack(pady=2)
        self.phone_entry = tk.Entry(self.win)
        self.phone_entry.pack()

        tk.Label(self.win, text=" Select Flight:", bg="#f0faff").pack(pady=5)
        flights = self.db.get_flights()

        self.flight_options = []
        self.flight_map = {}
        for f in flights:
            flight_id = f[0]
            seats_info = self.db.get_seat_info(flight_id)
            details = f"ID:{flight_id} | {f[1]} | {f[2]} | "
            details += " | ".join([f"{seat[0]}: ${seat[1]} (Seats: {seat[2]})" for seat in seats_info])
            self.flight_options.append(details)
            self.flight_map[details] = flight_id

        self.selected_flight = tk.StringVar()
        flight_dropdown = ttk.Combobox(self.win, textvariable=self.selected_flight, values=self.flight_options, state="readonly")
        flight_dropdown.pack(pady=5)

        tk.Label(self.win, text="Class:", bg="#f0faff").pack(pady=2)
        self.class_type = tk.StringVar()
        class_dropdown = ttk.Combobox(self.win, textvariable=self.class_type, values=["Economy", "First Class"], state="readonly")
        class_dropdown.pack()

        ttk.Button(self.win, text="Reserve", command=self.submit).pack(pady=15)

    def submit(self):
        try:
            name = self.name_entry.get().strip()
            passenger_id = self.id_entry.get().strip()
            phone = self.phone_entry.get().strip()
            flight_str = self.selected_flight.get()
            class_selected = self.class_type.get()

            if not (name and passenger_id and phone and flight_str and class_selected):
                messagebox.showerror(" Error", "Please fill all fields.")
                return

            if len(name.split()) < 3:
                messagebox.showerror(" Error", "Please enter full name with First, Middle, and Last name.")
                return

            if not (phone.isdigit() and len(phone) == 11):
                messagebox.showerror(" Error", "Phone number must be exactly 11 digits.")
                return

            if not (passenger_id.isdigit() and len(passenger_id) == 14):
                messagebox.showerror(" Error", "ID Number must be exactly 14 digits.")
                return

            flight_id = self.flight_map.get(flight_str)
            if not flight_id:
                messagebox.showerror(" Error", "Please select a valid flight.")
                return

            success = self.db.reserve_seat(flight_id, name, class_selected, passenger_id, phone)
            if success:
                messagebox.showinfo(" Success", "Seat reserved!")
                self.win.destroy()
            else:
                messagebox.showerror(" Error", "Seat not available or invalid class.")
        except Exception as e:
            messagebox.showerror(" Error", f"Unexpected error:\n{e}")
