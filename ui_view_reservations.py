import tkinter as tk

class ViewReservationsUI:
    def __init__(self, db):
        self.db = db

    def open(self, root):
        win = tk.Toplevel(root)
        win.title(" Reservations")
        win.geometry("650x400")
        win.configure(bg="#ffffff")

        reservations = self.db.get_reservations()
        for r in reservations:
            info = f" {r[0]} |  Destination: {r[1]} |  Date: {r[2]} | Class: {r[3]} |  Airline: {r[4]}"
            info += f"\n ID: {r[5]} |  Phone: {r[6]}\n"
            tk.Label(win, text=info, justify='left', bg="#ffffff", anchor='w', font=("Helvetica", 10)).pack(padx=10, pady=5, fill='x')
