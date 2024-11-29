import sqlite3
from datetime import datetime

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
        INSERT INTO guests_new (g_name, g_email, phone_number, g_birth_date, 
                              is_new_guest, guest_tc, gender, surname)
        SELECT g_name, g_email, phone_number, g_birth_date, 
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
        print(f"An error occurred: {e}")
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
        INSERT INTO dependents_new (TC_No, birth_date, name, gender, 
                                  relation_type, guest_id, primary_guest_id)
        SELECT TC_No, birth_date, name, gender, 
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
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_guests_table()
    fix_dependents_table()