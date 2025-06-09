import tkinter as tk
from tkinter import ttk, messagebox

class AddFlightUI:
    def __init__(self, db):
        self.db = db

    def open(self, root):
        self.win = tk.Toplevel(root)
        self.win.title("Add Flight")
        self.win.geometry("400x600")
        self.win.configure(bg="#f0faff")

        fields = ["Destination", "Date (YYYY-MM-DD)", "Airline", "Departure Time", "Arrival Time"]
        self.entries = []
        for field in fields:
            tk.Label(self.win, text=field + ":", bg="#f0faff", font=("Helvetica", 10)).pack(pady=2)
            entry = tk.Entry(self.win)
            entry.pack()
            self.entries.append(entry)

        tk.Label(self.win, text=" Meals on board? (1=Yes, 0=No)", bg="#f0faff").pack()
        self.meals_entry = tk.Entry(self.win)
        self.meals_entry.pack()

        tk.Label(self.win, text=" Direct flight? (1=Yes, 0=Transit)", bg="#f0faff").pack()
        self.direct_entry = tk.Entry(self.win)
        self.direct_entry.pack()

        self.seat_data = []
        for cls in ["Economy", "First Class"]:
            tk.Label(self.win, text=f"{cls} -  Price /  Seats", bg="#f0faff").pack(pady=2)
            price = tk.Entry(self.win)
            price.pack()
            seats = tk.Entry(self.win)
            seats.pack()
            self.seat_data.append((cls, price, seats))

        ttk.Button(self.win, text="Submit", command=self.submit).pack(pady=10)

    def submit(self):
        try:
            dest, date, airline, dep, arr = [e.get() for e in self.entries]
            meals, direct = int(self.meals_entry.get()), int(self.direct_entry.get())
            seats_info = [(cls, float(p.get()), int(s.get())) for cls, p, s in self.seat_data]
            self.db.add_flight(dest, date, airline, dep, arr, meals, direct, seats_info)
            messagebox.showinfo(" Success", "Flight added successfully!")
            self.win.destroy()
        except Exception as e:
            messagebox.showerror(" Error", f"Invalid input data.\n{e}")
