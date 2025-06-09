import sqlite3

class Database:
    def __init__(self, db_name="flights.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.ensure_reservations_schema()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination TEXT,
            date TEXT,
            airline TEXT,
            departure_time TEXT,
            arrival_time TEXT,
            meals INTEGER,
            is_direct INTEGER
        )''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS flight_seats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_id INTEGER,
            class_type TEXT,
            price REAL,
            total_seats INTEGER,
            available_seats INTEGER,
            FOREIGN KEY (flight_id) REFERENCES flights(id)
        )''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_id INTEGER,
            passenger_name TEXT,
            id_number TEXT,
            phone_number TEXT,
            FOREIGN KEY (flight_id) REFERENCES flights(id)
        )''')
        self.conn.commit()

    def ensure_reservations_schema(self):
        # التحقق مما إذا كان العمود class_type موجودًا في جدول reservations
        self.cursor.execute("PRAGMA table_info(reservations)")
        columns = [col[1] for col in self.cursor.fetchall()]
        if "class_type" not in columns:
            # إضافة عمود class_type إلى جدول reservations
            self.cursor.execute("ALTER TABLE reservations ADD COLUMN class_type TEXT")
            self.conn.commit()

    def add_flight(self, destination, date, airline, dep, arr, meals, direct, seats_data):
        self.cursor.execute('''
            INSERT INTO flights (destination, date, airline, departure_time, arrival_time, meals, is_direct)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (destination, date, airline, dep, arr, meals, direct))
        flight_id = self.cursor.lastrowid

        for seat in seats_data:  # [(class_type, price, total_seats)]
            self.cursor.execute('''
                INSERT INTO flight_seats (flight_id, class_type, price, total_seats, available_seats)
                VALUES (?, ?, ?, ?, ?)
            ''', (flight_id, seat[0], seat[1], seat[2], seat[2]))

        self.conn.commit()

    def get_flights(self):
        self.cursor.execute("SELECT * FROM flights")
        return self.cursor.fetchall()

    def get_seat_info(self, flight_id):
        self.cursor.execute("SELECT class_type, price, available_seats FROM flight_seats WHERE flight_id = ?", (flight_id,))
        return self.cursor.fetchall()

    def reserve_seat(self, flight_id, name, class_type, id_number, phone_number):
        self.cursor.execute("SELECT available_seats FROM flight_seats WHERE flight_id = ? AND class_type = ?", (flight_id, class_type))
        result = self.cursor.fetchone()
        if result and result[0] > 0:
            self.cursor.execute('''
                INSERT INTO reservations (flight_id, passenger_name, class_type, id_number, phone_number) 
                VALUES (?, ?, ?, ?, ?)
            ''', (flight_id, name, class_type, id_number, phone_number))
            self.cursor.execute('''
                UPDATE flight_seats SET available_seats = available_seats - 1 WHERE flight_id = ? AND class_type = ?
            ''', (flight_id, class_type))
            self.conn.commit()
            return True
        return False

    def get_reservations(self):
        self.cursor.execute('''
        SELECT r.passenger_name, f.destination, f.date, r.class_type, f.airline, r.id_number, r.phone_number
        FROM reservations r
        JOIN flights f ON r.flight_id = f.id
        ''')
        return self.cursor.fetchall()
