import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from db_control_sql import get_filtered_hotels, make_reservation, cancel_reservation, fetch_reservation_details

class HotelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Reservation System")
        self.root.geometry("800x600")

        self.selected_room = None
        self.dependent_entries = []
        self.main_menu()

    def main_menu(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main menu buttons
        tk.Label(self.root, text="Hotel Reservation System", font=("Arial", 20)).pack(pady=20)

        tk.Button(self.root, text="Make Reservation", width=20, command=self.make_reservation).pack(pady=10)
        tk.Button(self.root, text="Cancel Reservation", width=20, command=self.cancel_reservation).pack(pady=10)
        tk.Button(self.root, text="Get Reservation Info", width=20, command=self.get_reservation_info).pack(pady=10)

    def make_reservation(self):
        # Clear main menu and setup reservation interface
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main search frame
        search_frame = ttk.LabelFrame(self.root, text="Search Hotels", padding=15)
        search_frame.pack(fill='x', padx=10, pady=5)

        # Dates
        dates_frame = ttk.Frame(search_frame)
        dates_frame.pack(fill='x', pady=5)

        ttk.Label(dates_frame, text="Check-in Date:").grid(row=0, column=0, padx=5, pady=5)
        self.check_in_entry = DateEntry(dates_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.check_in_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(dates_frame, text="Check-out Date:").grid(row=0, column=2, padx=5, pady=5)
        self.check_out_entry = DateEntry(dates_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.check_out_entry.grid(row=0, column=3, padx=5, pady=5)

        # Filters
        filters_frame = ttk.Frame(search_frame)
        filters_frame.pack(fill='x', pady=5)

        ttk.Label(filters_frame, text="Hotel Type:").grid(row=0, column=0, padx=5, pady=5)
        self.hotel_type_combo = ttk.Combobox(filters_frame, values=['All', 'Lüks', 'İş', 'Resort', 'Butik', 'Ekonomik'],
                                             state='readonly', width=15)
        self.hotel_type_combo.grid(row=0, column=1, padx=5, pady=5)
        self.hotel_type_combo.set("All")

        ttk.Label(filters_frame, text="City:").grid(row=0, column=2, padx=5, pady=5)
        self.city_combo = ttk.Combobox(filters_frame,
                                       values=['All', 'İstanbul', 'Antalya', 'İzmir', 'Muğla', 'Ankara', 'Bursa', 'Aydın', 'Mersin'],
                                       state='readonly', width=15)
        self.city_combo.grid(row=0, column=3, padx=5, pady=5)
        self.city_combo.set("All")

        # Price range
        price_frame = ttk.Frame(search_frame)
        price_frame.pack(fill='x', pady=5)

        ttk.Label(price_frame, text="Price Range (TL):").pack(side='left', padx=5)
        self.price_min_entry = ttk.Entry(price_frame, width=10)
        self.price_min_entry.pack(side='left', padx=5)
        ttk.Label(price_frame, text="-").pack(side='left')
        self.price_max_entry = ttk.Entry(price_frame, width=10)
        self.price_max_entry.pack(side='left', padx=5)

        # Search button
        ttk.Button(search_frame, text="Search Hotels", command=self.search_hotels).pack(pady=10)
        ttk.Button(self.root, text="Back to Main Menu", command=self.main_menu).pack(pady=20)

    def search_hotels(self):
        try:
            # Validate dates
            check_in = self.check_in_entry.get_date()
            check_out = self.check_out_entry.get_date()
            if check_out <= check_in:
                messagebox.showerror("Invalid Dates", "Check-out date must be after check-in date")
                return

            # Validate price range
            price_min = float(self.price_min_entry.get()) if self.price_min_entry.get() else 0
            price_max = float(self.price_max_entry.get()) if self.price_max_entry.get() else float('inf')
            if price_max < price_min:
                messagebox.showerror("Invalid Price Range", "Maximum price must be greater than minimum price")
                return

            # Get hotels
            hotels = get_filtered_hotels(
                check_in=check_in,
                check_out=check_out,
                hotel_type=self.hotel_type_combo.get(),
                city=self.city_combo.get(),
                price_min=price_min,
                price_max=price_max
            )

            if not hotels:
                messagebox.showinfo("No Results", "No hotels found matching your criteria")
                return

            self.show_hotel_results(hotels)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_hotel_results(self, hotels):
        # Create results window
        hotels_window = tk.Toplevel(self.root)
        hotels_window.title("Available Hotels")
        hotels_window.geometry("800x600")

        # Create Treeview
        columns = ("Hotel Name", "Type", "Room Type", "Price per Night", "Room ID")
        hotels_tree = ttk.Treeview(hotels_window, columns=columns, show="headings")

        # Configure columns
        for col in columns:
            hotels_tree.heading(col, text=col)
            hotels_tree.column(col, width=150)

        # Insert data
        for hotel in hotels:
            hotels_tree.insert("", "end", values=hotel)

        hotels_tree.pack(fill="both", expand=True, padx=10, pady=10)

        def on_select(event):
            selected_item = hotels_tree.selection()
            if not selected_item:
                return

            item = hotels_tree.item(selected_item[0])
            values = item["values"]
            self.selected_room = {
                "hotel_name": values[0],
                "hotel_type": values[1],
                "room_type": values[2],
                "price": values[3],
                "room_id": values[4],
            }
            hotels_window.destroy()
            self.show_reservation_form()

        hotels_tree.bind("<<TreeviewSelect>>", on_select)

    def show_reservation_form(self):
        # Reservation form window
        reservation_window = tk.Toplevel(self.root)
        reservation_window.title("Make Reservation")
        reservation_window.geometry("800x600")

        # Guest information
        tk.Label(reservation_window, text=f"Hotel: {self.selected_room['hotel_name']}").pack(pady=5)
        tk.Label(reservation_window, text=f"Room Type: {self.selected_room['room_type']}").pack(pady=5)
        tk.Label(reservation_window, text=f"Price per Night: {self.selected_room['price']}").pack(pady=5)

        # Guest details
        guest_frame = ttk.Frame(reservation_window)
        guest_frame.pack(fill='x', pady=5)

        ttk.Label(guest_frame, text="Guest TC:").grid(row=0, column=0, padx=5, pady=5)
        guest_tc_entry = tk.Entry(guest_frame)
        guest_tc_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(guest_frame, text="Guest Name:").grid(row=1, column=0, padx=5, pady=5)
        guest_name_entry = tk.Entry(guest_frame)
        guest_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(guest_frame, text="Guest Surname:").grid(row=2, column=0, padx=5, pady=5)
        guest_surname_entry = tk.Entry(guest_frame)
        guest_surname_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(guest_frame, text="Email:").grid(row=3, column=0, padx=5, pady=5)
        email_entry = tk.Entry(guest_frame)
        email_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(guest_frame, text="Phone Number:").grid(row=4, column=0, padx=5, pady=5)
        phone_entry = tk.Entry(guest_frame)
        phone_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(guest_frame, text="Gender:").grid(row=5, column=0, padx=5, pady=5)
        gender_combo = ttk.Combobox(guest_frame, values=["M", "F"], state="readonly")
        gender_combo.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(guest_frame, text="Birth Date:").grid(row=6, column=0, padx=5, pady=5)
        birth_date_entry = DateEntry(guest_frame, width=12)
        birth_date_entry.grid(row=6, column=1, padx=5, pady=5)

        # Payment details
        payment_frame = ttk.Frame(reservation_window)
        payment_frame.pack(fill='x', pady=5)

        ttk.Label(payment_frame, text="Payment Method:").grid(row=0, column=0, padx=5, pady=5)
        payment_method_combo = ttk.Combobox(payment_frame, values=["Credit Card", "Cash", "Bank Transfer", "Online Payment"])
        payment_method_combo.grid(row=0, column=1, padx=5, pady=5)

        # Calculate total amount dynamically
        total_amount_label = tk.Label(payment_frame, text="Total Amount: 0 TL")
        total_amount_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Calculate total when dates or dependents change
        def update_total():
            try:
                check_in = self.check_in_entry.get_date()
                check_out = self.check_out_entry.get_date()
                num_nights = (check_out - check_in).days
                total = self.selected_room["price"] * num_nights
                total_amount_label.configure(text=f"Total Amount: {total} TL ({num_nights} days)")
            except Exception as e:
                print(f"Error calculating total: {e}")
                total_amount_label.configure(text="Total Amount: 0 TL")

        self.check_in_entry.bind("<<DateEntrySelected>>", lambda e: update_total())
        self.check_out_entry.bind("<<DateEntrySelected>>", lambda e: update_total())

        # Complete reservation button
        def complete_reservation():
            # Collect reservation data
            num_guests = 1 + len(self.dependent_entries)  # 1 for the main guest, +1 for each dependent
            reservation_data = {
                "main_guest": {
                    "tc": guest_tc_entry.get(),
                    "name": guest_name_entry.get(),
                    "surname": guest_surname_entry.get(),
                    "email": email_entry.get(),
                    "phone": phone_entry.get(),
                    "gender": gender_combo.get(),
                    "birth_date": birth_date_entry.get_date(),  # Birth date added
                },
                "check_in": self.check_in_entry.get_date(),
                "check_out": self.check_out_entry.get_date(),
                "room_info": {
                    "room_id": self.selected_room["room_id"],
                    "price": self.selected_room["price"],
                },
                "payment": {
                    "method": payment_method_combo.get(),
                    "amount": total_amount_label.cget("text").split(":")[1].strip().split()[0],
                    "date": datetime.now().date(),
                },
                "dependents": [],  # Empty list for dependents
                "num_guests": num_guests,
            }

            # Call the make_reservation function
            reservation_id = make_reservation(reservation_data)
            if reservation_id:
                messagebox.showinfo("Success", f"Reservation completed successfully! ID: {reservation_id}")
                reservation_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to complete reservation")

        tk.Button(reservation_window, text="Complete Reservation", command=complete_reservation).pack(pady=10)

    def cancel_reservation(self):
        # Cancel reservation logic
        cancel_window = tk.Toplevel(self.root)
        cancel_window.title("Cancel Reservation")
        cancel_window.geometry("400x300")

        tk.Label(cancel_window, text="Enter Reservation ID:").pack(pady=10)
        reservation_id_entry = tk.Entry(cancel_window)
        reservation_id_entry.pack(pady=5)

        tk.Label(cancel_window, text="Enter Guest TC:").pack(pady=10)
        guest_id_entry = tk.Entry(cancel_window)
        guest_id_entry.pack(pady=5)

        def cancel():
            reservation_id = reservation_id_entry.get().strip()
            guest_id = guest_id_entry.get().strip()

            if reservation_id and guest_id:
                print(f"Attempting to cancel reservation. ID: {reservation_id}, Guest ID: {guest_id}")
                result = cancel_reservation(reservation_id, guest_id)
                if result["success"]:
                    messagebox.showinfo("Success", result["message"])
                    cancel_window.destroy()
                else:
                    messagebox.showerror("Error", result["message"])
            else:
                messagebox.showerror("Error", "Please enter both Reservation ID and Guest ID")

        tk.Button(cancel_window, text="Cancel Reservation", command=cancel).pack(pady=20)

    def get_reservation_info(self):
        # Get reservation info logic
        info_window = tk.Toplevel(self.root)
        info_window.title("Get Reservation Info")
        info_window.geometry("400x300")

        tk.Label(info_window, text="Enter Reservation ID:").pack(pady=10)
        reservation_id_entry = tk.Entry(info_window)
        reservation_id_entry.pack(pady=5)

        tk.Label(info_window, text="Enter Guest ID:").pack(pady=10)
        guest_id_entry = tk.Entry(info_window)
        guest_id_entry.pack(pady=5)

        def fetch_info():
            reservation_id = reservation_id_entry.get()
            guest_id = guest_id_entry.get()

            if reservation_id and guest_id:
                reservation_info = fetch_reservation_details(reservation_id, guest_id)
                if reservation_info:
                    info_text = f"Reservation ID: {reservation_info['reservation_id']}\n"
                    info_text += f"Hotel: {reservation_info['hotel_name']}\n"
                    info_text += f"Check-in: {reservation_info['check_in']}\n"
                    info_text += f"Check-out: {reservation_info['check_out']}\n"
                    info_text += f"Status: {'Canceled' if reservation_info['is_canceled'] else 'Active'}"
                    messagebox.showinfo("Reservation Info", info_text)
                else:
                    messagebox.showerror("Error", "Reservation not found")
            else:
                messagebox.showerror("Error", "Please enter both Reservation ID and Guest ID")

        tk.Button(info_window, text="Get Reservation Info", command=fetch_info).pack(pady=20)

def main():
    root = tk.Tk()
    app = HotelApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
