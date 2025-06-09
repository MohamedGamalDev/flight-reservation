import tkinter as tk

class ViewFlightsUI:
    def __init__(self, db):
        self.db = db

    def open(self, root):
        win = tk.Toplevel(root)
        win.title(" All Flights")
        win.geometry("750x500")
        win.configure(bg="#ffffff")

        flights = self.db.get_flights()
        for f in flights:
            seats_info = self.db.get_seat_info(f[0])
            details = f"\n Destination: {f[1]} |  Airline: {f[3]} |  Date: {f[2]}\n"
            details += f" Departure: {f[4]} |  Arrival: {f[5]}\n"
            details += f" Meals: {'Yes' if f[6] else 'No'} |  {'Direct' if f[7] else 'Transit'}\n"
            for seat in seats_info:
                details += f"   {seat[0]} - ${seat[1]} | 🪑 Seats left: {seat[2]}\n"
            tk.Label(win, text=details, justify='left', bg="#ffffff", anchor='w', font=("Courier", 10)).pack(padx=10, pady=5, fill='x')
