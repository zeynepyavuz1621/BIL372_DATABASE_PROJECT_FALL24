import sqlite3
from datetime import datetime

# Veritabanı bağlantısı
def connect_db():
    return sqlite3.connect('HotelManagement.db', timeout=20)

def get_filtered_hotels(check_in, check_out, hotel_type="All", city="All", price_min=0, price_max=float('inf')):
    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = """
            SELECT 
                h.hotel_name,
                h.type,
                r.type as room_type,
                r.price_per_night,
                r.room_id
            FROM hotels h
            JOIN rooms r ON h.hotel_id = r.hotel_id
            LEFT JOIN reservations res ON r.room_id = res.room_id
            WHERE (res.arrival_date <= ? OR res.departure_date <= ? OR res.reservation_id IS NULL)
        """

        params = [check_in, check_out]
        
        if hotel_type != "All":
            query += " AND h.type = ?"
            params.append(hotel_type)
        
        if city != "All":
            query += " AND h.city = ?"
            params.append(city)
        
        if price_min > 0:
            query += " AND r.price_per_night >= ?"
            params.append(price_min)
        
        if price_max < float('inf'):
            query += " AND r.price_per_night <= ?"
            params.append(price_max)

        query += " GROUP BY h.hotel_name, r.type"
        
        cursor.execute(query, params)
        return cursor.fetchall()

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
        
    finally:
        if conn:
            conn.close()

def make_reservation(reservation_data):
    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        # Enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Start transaction
        cursor.execute("BEGIN TRANSACTION")
        
        # Extract data
        guest_info = reservation_data["main_guest"]
        check_in = reservation_data["check_in"]
        check_out = reservation_data["check_out"]
        dependents = reservation_data["dependents"]
        payment = reservation_data["payment"]
        room_info = reservation_data["room_info"]
        
        # 1. Check if guest already exists
        cursor.execute("""
            SELECT guest_id FROM guests 
            WHERE guest_tc = ?
        """, (guest_info["tc"],))
        
        existing_guest = cursor.fetchone()
        
        if existing_guest:
            guest_id = existing_guest[0]
            # Update existing guest information
            cursor.execute("""
                UPDATE guests 
                SET g_name = ?, g_email = ?, phone_number = ?, 
                    g_birth_date = ?, is_new_guest = ?, gender = ?, surname = ?
                WHERE guest_id = ?
            """, (
                guest_info["name"],
                guest_info["email"],
                guest_info["phone"],
                guest_info["birth_date"],
                False,  # existing guest
                guest_info["gender"],
                guest_info["surname"],
                guest_id
            ))
        else:
            # Insert new guest
            cursor.execute("""
                INSERT INTO guests (
                    g_name, g_email, phone_number, g_birth_date,
                    is_new_guest, guest_tc, gender, surname
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                guest_info["name"],
                guest_info["email"],
                guest_info["phone"],
                guest_info["birth_date"],
                True,
                guest_info["tc"],
                guest_info["gender"],
                guest_info["surname"]
            ))
            guest_id = cursor.lastrowid

        # 2. Create reservation with the correct guest_id
        cursor.execute("""
            INSERT INTO reservations (
                arrival_date, departure_date, arrival_time, exit_time,
                num_guests, is_canceled, guest_id, room_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            check_in,
            check_out,
            "14:00:00",  # Standard check-in time
            "11:00:00",  # Standard check-out time
            reservation_data["num_guests"],
            False,
            guest_id,  # Using the correct guest_id
            room_info["room_id"]
        ))
        reservation_id = cursor.lastrowid
        
        # 3. Add dependents with proper references
        for dep in dependents:
            cursor.execute("""
                INSERT INTO dependents (
                    TC_No, birth_date, name, gender,
                    relation_type, guest_id, primary_guest_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                dep["tc"],
                dep["birth_date"],
                dep["name"],
                dep["gender"],
                dep["relation_type"],
                guest_id,  # Using the correct guest_id
                guest_id   # primary_guest_id is the same as guest_id
            ))
        
        # 4. Create payment record
        cursor.execute("""
            INSERT INTO payments (
                PaymentMethod, Amount, PaymentDate,
                Status, room_id, reservation_id
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            payment["method"],
            payment["amount"],
            payment["date"],
            'Completed',
            room_info["room_id"],
            reservation_id
        ))
        
        # 5. Update room availability
        cursor.execute("""
            UPDATE rooms
            SET is_available = ?
            WHERE room_id = ?
        """, (False, room_info["room_id"]))
        
        # Commit transaction
        conn.commit()
        return reservation_id
        
    except sqlite3.Error as e:
        print(f"Database error in make_reservation: {e}")
        if conn:
            conn.rollback()
        return -1
        
    finally:
        if conn:
            conn.close()

def get_reservation(reservation_id):
    """Helper function to verify reservation data"""
    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        query = """
            SELECT r.*, g.g_name, g.guest_tc, d.name as dependent_name
            FROM reservations r
            JOIN guests g ON r.guest_id = g.guest_id
            LEFT JOIN dependents d ON g.guest_id = d.guest_id
            WHERE r.reservation_id = ?
        """
        
        cursor.execute(query, (reservation_id,))
        return cursor.fetchall()
        
    except sqlite3.Error as e:
        print(f"Database error in get_reservation: {e}")
        return None
        
    finally:
        if conn:
            conn.close()
def cancel_reservation(reservation_id, guest_id):
    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        # Enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")
        # Start transaction
        cursor.execute("BEGIN TRANSACTION")
        # Check if reservation exists and is not already cancelled
        cursor.execute("""
            SELECT r.*, rm.price_per_night
            FROM reservations r
            JOIN rooms rm ON r.room_id = rm.room_id
            WHERE r.reservation_id = ? AND r.guest_id = ? AND r.is_canceled = 0
        """, (reservation_id, guest_id))
        reservation = cursor.fetchone()
        if not reservation:
            return {
                'success': False,
                'message': "Reservation not found or already cancelled."
            }
        # Calculate cancellation fee (20% of total amount)
        arrival_date = datetime.strptime(reservation[1], '%Y-%m-%d').date()
        departure_date = datetime.strptime(reservation[2], '%Y-%m-%d').date()
        stay_duration = (departure_date - arrival_date).days
        total_amount = reservation[-1] * stay_duration # price_per_night * duration
        cancellation_fee = total_amount * 0.2
        # Update reservation status
        cursor.execute("""
            UPDATE reservations
            SET is_canceled = 1
            WHERE reservation_id = ? AND guest_id = ?
        """, (reservation_id, guest_id))
        # Add cancellation payment record
        cursor.execute("""
            INSERT INTO payments (
                PaymentMethod, Amount, PaymentDate,
                Status, room_id, reservation_id
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            'Cancellation Fee',
            cancellation_fee,
            datetime.now().date(),
            'Cancelled',
            reservation[9], # room_id
            reservation_id
        ))
        # Make room available again
        cursor.execute("""
            UPDATE rooms
            SET is_available = 1
            WHERE room_id = ?
        """, (reservation[9],)) # room_id
        conn.commit()
        return {
            'success': True,
            'message': f"Reservation cancelled successfully.\nCancellation fee: {cancellation_fee:.2f} TL",
            'cancellation_fee': cancellation_fee
        }
    except sqlite3.Error as e:
        print(f"Database error in cancel_reservation: {e}")
        if conn:
            conn.rollback()
        return {
            'success': False,
            'message': f"An error occurred: {str(e)}"
        }
    finally:
        if conn:
            conn.close()