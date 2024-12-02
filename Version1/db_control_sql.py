import sqlite3
from datetime import datetime


# Veritabanı bağlantısı
def connect_db():
    return sqlite3.connect('HotelManagement.db')

def get_filtered_hotels(check_in, check_out, hotel_type="All", city="All", price_min=0, price_max=float('inf')):
    conn = None
    try:
        conn = sqlite3.connect('HotelManagement.db', timeout=20)
        cursor = conn.cursor()

        query = """
            SELECT 
                h.hotel_id,
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

        query += " GROUP BY h.hotel_name,r.type"
        
        cursor.execute(query, params)
        return cursor.fetchall()

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
        
    finally:
        if conn:
            conn.close()
import sqlite3
from datetime import datetime

def make_reservation(reservation_data):
    conn = None
    try:
        conn = sqlite3.connect('HotelManagement.db', timeout=20)
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
        '''return True'''
        return reservation_id
        
    except sqlite3.Error as e:
        print(f"Database error in make_reservation: {e}")
        if conn:
            conn.rollback()
        return False
        
    finally:
        if conn:
            conn.close()

def get_reservation(reservation_id):
    """Helper function to verify reservation data"""
    conn = None
    try:
        conn = sqlite3.connect('HotelManagement.db', timeout=20)
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

            
def connect_db():
    """Create a new database connection with extended timeout"""
    return sqlite3.connect('HotelManagement.db', timeout=20)



def fetch_guest_id_by_tc(guest_tc):
    """
    TC numarasından guest ID'yi bulan fonksiyon
    """
    conn = None
    try:
        conn = sqlite3.connect('HotelManagement.db', timeout=20)
        cursor = conn.cursor()
        
        query = "SELECT guest_id FROM guests WHERE guest_tc = ?"
        cursor.execute(query, (guest_tc,))
        result = cursor.fetchone()
        
        return result[0] if result else None
        
    except sqlite3.Error as e:
        print(f"Database error in fetch_guest_id_by_tc: {e}")
        return None
    finally:
        if conn:
            conn.close()

def fetch_dependent_details(guest_id):
    """
    Guest ID'ye göre dependent bilgilerini getiren fonksiyon
    """
    conn = None
    try:
        conn = sqlite3.connect('HotelManagement.db', timeout=20)
        cursor = conn.cursor()
        
        query = """
            SELECT 
                dependent_id,
                TC_No,
                birth_date,
                name,
                gender,
                relation_type,
                guest_id,
                primary_guest_id
            FROM dependents
            WHERE primary_guest_id = ?
        """
        
        cursor.execute(query, (guest_id,))
        dependents = cursor.fetchall()
        
        if dependents:
            return [
                {
                    "dependent_id": dep[0],
                    "tc_no": dep[1],
                    "birth_date": dep[2],
                    "name": dep[3],
                    "gender": dep[4],
                    "relation_type": dep[5],
                    "guest_id": dep[6],
                    "primary_guest_id": dep[7]
                }
                for dep in dependents
            ]
        return None
        
    except sqlite3.Error as e:
        print(f"Database error in fetch_dependent_details: {e}")
        return None
    finally:
        if conn:
            conn.close()



def fetch_reservation_details(reservation_id, customer_tc):
    """
    Fetch detailed reservation information based on reservation ID and customer name.
    """
    conn = None
    try:
        # Connect to the database
        conn = sqlite3.connect('HotelManagement.db', timeout=20)
        cursor = conn.cursor()

        # SQL query to fetch reservation details
        query = """
            SELECT 
                r.reservation_id,
                r.arrival_date,
                r.departure_date,
                r.num_guests,
                r.is_canceled,
                g.g_name AS guest_name,
                g.surname AS guest_surname,
                g.guest_tc,
                g.phone_number,
                g.g_email,
                h.hotel_name,
                rm.type AS room_type,
                rm.price_per_night
            FROM reservations r
            JOIN guests g ON r.guest_id = g.guest_id
            JOIN rooms rm ON r.room_id = rm.room_id
            JOIN hotels h ON rm.hotel_id = h.hotel_id
            WHERE r.reservation_id = ? AND guest_tc = ?
        """
        
        # Debugging: Print the query and parameters
        print(f"Executing query: {query} with values: {reservation_id}, {customer_tc}")
        
        # Execute query with provided parameters
        cursor.execute(query, (reservation_id, customer_tc))
        
        # Fetch the reservation details
        reservation_details = cursor.fetchone()

        # Debugging: Print the result
        print(f"Query result: {reservation_details}")

        if reservation_details:
            # Return reservation details as a dictionary
            keys = [
                "reservation_id", "check_in", "check_out", "num_guests", "is_canceled",
                "guest_name", "guest_surname", "guest_tc", "phone_number", "email",
                "hotel_name", "room_type", "price_per_night"
            ]
            return dict(zip(keys, reservation_details))
        else:
            print("No matching reservation found.")
            return None

    except sqlite3.Error as e:
        print(f"Database error in fetch_reservation_details: {e}")
        return None

    finally:
        if conn:
            conn.close()
def cancel_reservation(reservation_id, guest_tc):
    conn = None
    try:
        conn = connect_db()  # Assuming connect_db() is defined to connect to your DB
        cursor = conn.cursor()

        # Enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")

        # Start transaction
        cursor.execute("BEGIN TRANSACTION")

        # Check if reservation exists and is not already cancelled, using guest_tc
        cursor.execute("""
            SELECT r.*, rm.price_per_night
            FROM reservations r
            JOIN rooms rm ON r.room_id = rm.room_id
            JOIN guests g ON r.guest_id = g.guest_id
            WHERE r.reservation_id = ? AND g.guest_tc = ? AND r.is_canceled = 0
        """, (reservation_id, guest_tc))

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
        total_amount = reservation[-1] * stay_duration  # price_per_night * duration
        cancellation_fee = total_amount * 0.2

        # Update reservation status to cancelled using guest_tc
        cursor.execute("""
            UPDATE reservations
            SET is_canceled = 1
            WHERE reservation_id = ? AND guest_id = (SELECT guest_id FROM guests WHERE guest_tc = ?)
        """, (reservation_id, guest_tc))

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
            reservation[9],  # room_id
            reservation_id
        ))

        # Make room available again
        cursor.execute("""
            UPDATE rooms
            SET is_available = 1
            WHERE room_id = ?
        """, (reservation[9],))  # room_id

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
def make_comment_in_db(current_date, hotel_name, guest_tc, comment, rating):
    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("BEGIN TRANSACTION")
        
        # First verify guest exists and get guest_id
        cursor.execute("""
            SELECT guest_id, g_name 
            FROM guests 
            WHERE guest_tc = ?
        """, (guest_tc,))
        guest_result = cursor.fetchone()
        
        if not guest_result:
            print(f"Guest not found with TC: {guest_tc}")
            return {
                'success': False,
                'message': "Guest not found. Please check your TC number."
            }
        
        # Get hotel_id from hotel_name
        cursor.execute("""
            SELECT hotel_id 
            FROM hotels 
            WHERE hotel_name = ?
        """, (hotel_name,))
        hotel_result = cursor.fetchone()
        
        if not hotel_result:
            print(f"Hotel not found with name: {hotel_name}")
            return {
                'success': False,
                'message': "Hotel not found. Please try again."
            }
        
        guest_id = guest_result[0]
        hotel_id = hotel_result[0]
        
        # Add the comment
        cursor.execute("""
            INSERT INTO comments (
                date,
                content,
                num_stars,
                guest_id,
                hotel_id
            ) VALUES (?, ?, ?, ?, ?)
        """, (current_date, comment, rating, guest_id, hotel_id))
        
        conn.commit()
        print(f"Comment added successfully by guest {guest_result[1]} for hotel {hotel_name}")
        
        return {
            'success': True,
            'message': "Comment added successfully!"
        }
        
    except sqlite3.IntegrityError as ie:
        print(f"Integrity error in make_comment_in_db: {ie}")
        if conn:
            conn.rollback()
        return {
            'success': False,
            'message': "Database integrity error. Please ensure all information is correct."
        }
        
    except sqlite3.Error as e:
        print(f"Database error in make_comment_in_db: {e}")
        if conn:
            conn.rollback()
        return {
            'success': False,
            'message': "A database error occurred. Please try again."
        }
        
    except Exception as e:
        print(f"Unexpected error in make_comment_in_db: {e}")
        if conn:
            conn.rollback()
        return {
            'success': False,
            'message': f"An unexpected error occurred: {str(e)}"
        }
        
    finally:
        if conn:
            conn.close()
def get_hotel_photos():
    conn = None
    try:
        conn = sqlite3.connect('HotelManagement.db')
        cursor = conn.cursor()

        query = '''
            SELECT *
            FROM photos
            WHERE image_type='exterior'
        '''
        
        cursor.execute(query)
        return cursor.fetchall()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
        
    finally:
        if conn:
            conn.close()
def get_room_photos(hotel_id):
    conn = None
    try:
        conn = sqlite3.connect('HotelManagement.db')
        cursor = conn.cursor()

        # Use explicit JOIN syntax for clarity
        query = '''
            SELECT p.image_id, p.image_path
            FROM photos AS p
            INNER JOIN hotels AS h ON p.hotel_id = h.hotel_id
            WHERE p.image_type = 'room' AND h.hotel_id = ?
        '''
        
        cursor.execute(query, (hotel_id,))
        return cursor.fetchall()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
        
    finally:
        if conn:
            conn.close()
def get_comments(hotel_id):
    conn = None
    try:
        conn = sqlite3.connect('HotelManagement.db')
        cursor = conn.cursor()
        
        query = """
            SELECT 
                c.comment_id,
                c.date,
                c.content,
                c.num_stars,
                g.g_name || ' ' || g.surname as guest_name,
                h.hotel_name,
                g.guest_tc
            FROM comments c
            JOIN guests g ON c.guest_id = g.guest_id
            JOIN hotels h ON c.hotel_id = h.hotel_id
            WHERE c.hotel_id = ?
            ORDER BY c.date DESC
        """
        
        cursor.execute(query, (hotel_id,))
        comments = cursor.fetchall()
        
        # Convert the results to a list of dictionaries
        formatted_comments = []
        for comment in comments:
            formatted_comments.append({
                'comment_id': comment[0],
                'date': comment[1],
                'text': comment[2],
                'rating': comment[3],
                'guest_name': comment[4],
                'hotel_name': comment[5],
                'guest_tc': comment[6]
            })
            
        return formatted_comments
        
    except sqlite3.Error as e:
        print(f"Database error in get_comments: {e}")
        return []
        
    finally:
        if conn:
            conn.close()