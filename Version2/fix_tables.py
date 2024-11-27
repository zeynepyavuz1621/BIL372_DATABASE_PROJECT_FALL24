import sqlite3

def fix_guests_table():
    conn = sqlite3.connect('HotelManagement.db')
    cursor = conn.cursor()
    try:
        # Start transaction
        cursor.execute("BEGIN TRANSACTION")
        
        # Create temporary table with correct structure
        cursor.execute("""
            CREATE TABLE guests_new (
                guest_id INTEGER PRIMARY KEY AUTOINCREMENT,
                g_name TEXT,
                g_email TEXT,
                phone_number TEXT,
                g_birth_date DATE,
                is_new_guest BOOLEAN,
                guest_tc TEXT UNIQUE,
                gender TEXT,
                surname TEXT
            )
        """)
        
        # Copy data from old table to new table
        cursor.execute("""
            INSERT INTO guests_new (guest_id, g_name, g_email, phone_number, g_birth_date,
                is_new_guest, guest_tc, gender, surname)
            SELECT guest_id, g_name, g_email, phone_number, g_birth_date,
                is_new_guest, guest_tc, gender, surname
            FROM guests
        """)
        
        # Drop old table
        cursor.execute("DROP TABLE guests")
        
        # Rename new table to guests
        cursor.execute("ALTER TABLE guests_new RENAME TO guests")
        
        # Create index on guest_tc for faster lookups
        cursor.execute("CREATE INDEX idx_guest_tc ON guests(guest_tc)")
        
        # Commit changes
        conn.commit()
        print("Successfully restructured guests table")
        
    except sqlite3.Error as e:
        print(f"An error occurred in guests table: {e}")
        conn.rollback()
    finally:
        conn.close()

def fix_dependents_table():
    conn = sqlite3.connect('HotelManagement.db')
    cursor = conn.cursor()
    try:
        # Start transaction
        cursor.execute("BEGIN TRANSACTION")
        
        # Create temporary table with correct structure
        cursor.execute("""
            CREATE TABLE dependents_new (
                dependent_id INTEGER PRIMARY KEY AUTOINCREMENT,
                TC_No TEXT UNIQUE,
                birth_date DATE,
                name TEXT,
                gender TEXT,
                relation_type TEXT,
                guest_id INTEGER,
                primary_guest_id INTEGER,
                FOREIGN KEY (guest_id) REFERENCES guests(guest_id),
                FOREIGN KEY (primary_guest_id) REFERENCES guests(guest_id)
            )
        """)
        
        # Copy data from old table to new table
        cursor.execute("""
            INSERT INTO dependents_new (dependent_id, TC_No, birth_date, name, gender,
                relation_type, guest_id, primary_guest_id)
            SELECT dependent_id, TC_No, birth_date, name, gender,
                relation_type, guest_id, primary_guest_id
            FROM dependents
        """)
        
        # Drop old table
        cursor.execute("DROP TABLE dependents")
        
        # Rename new table to dependents
        cursor.execute("ALTER TABLE dependents_new RENAME TO dependents")
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX idx_dependent_tc ON dependents(TC_No)")
        cursor.execute("CREATE INDEX idx_dependent_guest ON dependents(guest_id)")
        
        # Commit changes
        conn.commit()
        print("Successfully restructured dependents table")
        
    except sqlite3.Error as e:
        print(f"An error occurred in dependents table: {e}")
        conn.rollback()
    finally:
        conn.close()

def fix_reservations_table():
    conn = sqlite3.connect('HotelManagement.db')
    cursor = conn.cursor()
    try:
        # Start transaction
        cursor.execute("BEGIN TRANSACTION")
        
        # Create temporary table with correct structure
        cursor.execute("""
            CREATE TABLE reservations_new (
                reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                arrival_date DATE,
                departure_date DATE,
                arrival_time TIME,
                exit_time TIME,
                num_guests INTEGER,
                is_canceled BOOLEAN,
                guest_id INTEGER,
                room_id INTEGER,
                FOREIGN KEY (guest_id) REFERENCES guests(guest_id),
                FOREIGN KEY (room_id) REFERENCES rooms(room_id)
            )
        """)
        
        # Copy data from old table to new table
        cursor.execute("""
            INSERT INTO reservations_new (reservation_id, arrival_date, departure_date, 
                arrival_time, exit_time, num_guests, is_canceled, guest_id, room_id)
            SELECT reservation_id, arrival_date, departure_date, arrival_time, exit_time,
                num_guests, is_canceled, guest_id, room_id
            FROM reservations
        """)
        
        # Drop old table
        cursor.execute("DROP TABLE reservations")
        
        # Rename new table to reservations
        cursor.execute("ALTER TABLE reservations_new RENAME TO reservations")
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX idx_reservation_guest ON reservations(guest_id)")
        cursor.execute("CREATE INDEX idx_reservation_room ON reservations(room_id)")
        cursor.execute("CREATE INDEX idx_reservation_dates ON reservations(arrival_date, departure_date)")
        
        # Commit changes
        conn.commit()
        print("Successfully restructured reservations table")
        
    except sqlite3.Error as e:
        print(f"An error occurred in reservations table: {e}")
        conn.rollback()
    finally:
        conn.close()

def check_database_state():
    conn = sqlite3.connect('HotelManagement.db')
    cursor = conn.cursor()
    
    try:
        # Tablo listesini al
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("\nCurrent database state:")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"{table_name}: {count} records")
            
    except sqlite3.Error as e:
        print(f"Error checking database state: {e}")
    finally:
        conn.close()
def fix_rooms_table():
    conn = sqlite3.connect('HotelManagement.db')
    cursor = conn.cursor()
    try:
        cursor.execute("BEGIN TRANSACTION")
        
        # Create temporary table with correct structure
        cursor.execute("""
            CREATE TABLE rooms_new (
                room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_number TEXT,
                type TEXT,
                has_balcony BOOLEAN,
                has_sea_view BOOLEAN,
                r_capacity INTEGER,
                price_per_night REAL,
                floor INTEGER,
                hotel_id INTEGER,
                is_available BOOLEAN,
                FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id)
            )
        """)
        
        # Copy data from old table to new table
        cursor.execute("""
            INSERT INTO rooms_new (room_id, room_number, type, has_balcony, has_sea_view,
                r_capacity, price_per_night, floor, hotel_id, is_available)
            SELECT room_id, room_number, type, has_balcony, has_sea_view,
                r_capacity, price_per_night, floor, hotel_id, is_available
            FROM rooms
        """)
        
        # Drop old table
        cursor.execute("DROP TABLE rooms")
        
        # Rename new table to rooms
        cursor.execute("ALTER TABLE rooms_new RENAME TO rooms")
        
        # Create indexes
        cursor.execute("CREATE INDEX idx_room_hotel ON rooms(hotel_id)")
        
        conn.commit()
        print("Successfully restructured rooms table")
        
    except sqlite3.Error as e:
        print(f"An error occurred in rooms table: {e}")
        conn.rollback()
    finally:
        conn.close()
if __name__ == "__main__":
    print("Starting database table fixes...")
    
    print("\nChecking initial database state...")
    check_database_state()
    
    print("\nFixing rooms table...")  # Önce rooms tablosunu düzelt
    fix_rooms_table()
    
    print("\nFixing guests table...")
    fix_guests_table()
    
    print("\nFixing dependents table...")
    fix_dependents_table()
    
    print("\nFixing reservations table...")
    fix_reservations_table()
    
    print("\nChecking final database state...")
    check_database_state()
    
    print("\nAll fixes completed!")