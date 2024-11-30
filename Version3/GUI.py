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
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Hotel Reservation System", font=("Arial", 20)).pack(pady=20)
        tk.Button(self.root, text="Make Reservation", width=20, command=self.make_reservation).pack(pady=10)
        tk.Button(self.root, text="Cancel Reservation", width=20, command=self.cancel_reservation).pack(pady=10)
        tk.Button(self.root, text="Get Reservation Info", width=20, command=self.get_reservation_info).pack(pady=10)

    def make_reservation(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        search_frame = ttk.LabelFrame(self.root, text="Search Hotels", padding=15)
        search_frame.pack(fill='x', padx=10, pady=5)

        dates_frame = ttk.Frame(search_frame)
        dates_frame.pack(fill='x', pady=5)

        ttk.Label(dates_frame, text="Check-in Date:").grid(row=0, column=0, padx=5, pady=5)
        self.check_in_entry = DateEntry(dates_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.check_in_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(dates_frame, text="Check-out Date:").grid(row=0, column=2, padx=5, pady=5)
        self.check_out_entry = DateEntry(dates_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.check_out_entry.grid(row=0, column=3, padx=5, pady=5)

        filters_frame = ttk.Frame(search_frame)
        filters_frame.pack(fill='x', pady=5)

        ttk.Label(filters_frame, text="Hotel Type:").grid(row=0, column=0, padx=5, pady=5)
        self.hotel_type_combo = ttk.Combobox(filters_frame, values=['All', 'Lüks', 'İş', 'Resort', 'Butik', 'Ekonomik'],
                                             state='readonly', width=15)
        self.hotel_type_combo.grid(row=0, column=1, padx=5, pady=5)
        self.hotel_type_combo.set("All")

        ttk.Label(filters_frame, text="City:").grid(row=0, column=2, padx=5, pady=5)
        self.city_combo = ttk.Combobox(filters_frame, values=['All', 'İstanbul', 'Antalya', 'İzmir', 'Muğla', 'Ankara', 'Bursa', 'Aydın', 'Mersin'],
                                       state='readonly', width=15)
        self.city_combo.grid(row=0, column=3, padx=5, pady=5)
        self.city_combo.set("All")

        ttk.Label(filters_frame, text="Number of Guests:").grid(row=1, column=0, padx=5, pady=5)
        self.guest_number_entry = ttk.Entry(filters_frame, width=10)
        self.guest_number_entry.grid(row=1, column=1, padx=5, pady=5)

        price_frame = ttk.Frame(search_frame)
        price_frame.pack(fill='x', pady=5)

        ttk.Label(price_frame, text="Price Range (TL):").pack(side='left', padx=5)
        self.price_min_entry = ttk.Entry(price_frame, width=10)
        self.price_min_entry.pack(side='left', padx=5)
        ttk.Label(price_frame, text="-").pack(side='left')
        self.price_max_entry = ttk.Entry(price_frame, width=10)
        self.price_max_entry.pack(side='left', padx=5)

        ttk.Button(search_frame, text="Search Hotels", command=self.search_hotels).pack(pady=10)
        ttk.Button(self.root, text="Back to Main Menu", command=self.main_menu).pack(pady=20)

    def search_hotels(self):
        try:
            check_in = self.check_in_entry.get_date()
            check_out = self.check_out_entry.get_date()
            if check_out <= check_in:
                messagebox.showerror("Invalid Dates", "Check-out date must be after check-in date")
                return

            try:
                guest_number = int(self.guest_number_entry.get())
                if guest_number <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid Guest Number", "Please enter a valid number of guests")
                return

            price_min = float(self.price_min_entry.get()) if self.price_min_entry.get() else 0
            price_max = float(self.price_max_entry.get()) if self.price_max_entry.get() else float('inf')
            if price_max < price_min:
                messagebox.showerror("Invalid Price Range", "Maximum price must be greater than minimum price")
                return

            hotels = get_filtered_hotels(
                check_in=check_in,
                check_out=check_out,
                hotel_type=self.hotel_type_combo.get(),
                city=self.city_combo.get(),
                price_min=price_min,
                price_max=price_max,
                guest_number=guest_number
            )

            if not hotels:
                messagebox.showinfo("No Results", "No hotels found matching your criteria")
                return

            self.show_hotel_results(hotels)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_hotel_results(self, hotels):
        hotels_window = tk.Toplevel(self.root)
        hotels_window.title("Available Hotels")
        hotels_window.geometry("800x600")

        columns = ("Hotel Name", "Type", "Room Type", "Price per Night", "Room ID")
        hotels_tree = ttk.Treeview(hotels_window, columns=columns, show="headings")

        for col in columns:
            hotels_tree.heading(col, text=col)
            hotels_tree.column(col, width=150)

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

        # Guest fields
        self.guest_entries = {}

        ttk.Label(guest_frame, text="Guest TC:").grid(row=0, column=0, padx=5, pady=5)
        guest_tc_entry = tk.Entry(guest_frame)
        guest_tc_entry.grid(row=0, column=1, padx=5, pady=5)
        self.guest_entries['tc'] = guest_tc_entry;

        ttk.Label(guest_frame, text="Guest Name:").grid(row=1, column=0, padx=5, pady=5)
        guest_name_entry = tk.Entry(guest_frame)
        guest_name_entry.grid(row=1, column=1, padx=5, pady=5)
        self.guest_entries['name'] = guest_name_entry;

        ttk.Label(guest_frame, text="Guest Surname:").grid(row=2, column=0, padx=5, pady=5)
        guest_surname_entry = tk.Entry(guest_frame)
        guest_surname_entry.grid(row=2, column=1, padx=5, pady=5)
        self.guest_entries['surname'] = guest_surname_entry;

        ttk.Label(guest_frame, text="Email:").grid(row=3, column=0, padx=5, pady=5)
        email_entry = tk.Entry(guest_frame)
        email_entry.grid(row=3, column=1, padx=5, pady=5)
        self.guest_entries['email'] = email_entry;

        ttk.Label(guest_frame, text="Phone Number:").grid(row=4, column=0, padx=5, pady=5)
        phone_entry = tk.Entry(guest_frame)
        phone_entry.grid(row=4, column=1, padx=5, pady=5)
        self.guest_entries['phone'] = phone_entry;

        ttk.Label(guest_frame, text="Gender:").grid(row=5, column=0, padx=5, pady=5)
        gender_combo = ttk.Combobox(guest_frame, values=["M", "F"], state="readonly")
        gender_combo.grid(row=5, column=1, padx=5, pady=5)
        self.guest_entries['gender'] = gender_combo;

        ttk.Label(guest_frame, text="Birth Date:").grid(row=6, column=0, padx=5, pady=5)
        birth_date_entry = DateEntry(guest_frame, width=12)
        birth_date_entry.grid(row=6, column=1, padx=5, pady=5)
        self.guest_entries['birth_date'] = birth_date_entry;

        # Payment details
        payment_frame = ttk.Frame(reservation_window)
        payment_frame.pack(fill='x', pady=5)

        ttk.Label(payment_frame, text="Payment Method:").grid(row=0, column=0, padx=5, pady=5)
        self.payment_method_combo = ttk.Combobox(payment_frame, values=["Credit Card", "Cash", "Bank Transfer", "Online Payment"])
        self.payment_method_combo.grid(row=0, column=1, padx=5, pady=5)

        # Calculate total amount dynamically
        self.total_amount_label = tk.Label(payment_frame, text="Total Amount: 0 TL")
        self.total_amount_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Complete reservation button
        ttk.Button(reservation_window, text="Complete Reservation", 
                  command=self.complete_reservation).pack(pady=10)

        # Set up event bindings
        self.setup_event_bindings()
        # Calculate initial total
        self.update_total()

    def setup_event_bindings(self):
        self.check_in_entry.bind("<<DateEntrySelected>>", self.update_total)
        self.check_out_entry.bind("<<DateEntrySelected>>", self.update_total)

    def update_total(self, *args):
        """
        Calculate the total amount based on the check-in and check-out dates, 
        the selected room price, and the number of dependents.
        """
        try:
            # Get dates from DateEntry widgets
            check_in = self.check_in_entry.get_date()
            check_out = self.check_out_entry.get_date()
            
            # Calculate the number of nights
            num_nights = (check_out - check_in).days

            if num_nights <= 0:  # Invalid case
                self.total_amount_label.configure(text="Total: 0 TL")
                return

            # Ensure the room price is numeric
            room_price = float(self.selected_room['price'])
            
            # Calculate total amount (room price x nights x number of people)
            total = room_price * num_nights * (len(self.dependent_entries) + 1)
            
            # Update the label with the formatted total
            self.total_amount_label.configure(text=f"Total: {total:.2f} TL")

        except Exception as e:
            print(f"Error calculating total: {e}")
            self.total_amount_label.configure(text="Total: 0 TL")

    def complete_reservation(self):
        try:
            # Validate main guest information
            if not all(entry.get() for entry in self.guest_entries.values()):
                messagebox.showerror("Error", "Please fill in all main guest information")
                return

            # Get dependents information
            dependents = []
            for dep in self.dependent_entries:
                if not all(entry.get() for entry in dep['entries'].values()):
                    messagebox.showerror("Error", "Please fill in all dependent information or remove incomplete dependents")
                    return

                dependent_data = {
                    'tc': dep['entries']['tc'].get(),
                    'name': dep['entries']['name'].get(),
                    'birth_date': dep['entries']['birth_date'].get_date(),
                    'gender': dep['entries']['gender'].get(),
                    'relation_type': dep['entries']['relation_type'].get()
                }
                dependents.append(dependent_data)

            # Create reservation data
            reservation_data = {
                "main_guest": {
                    'tc': self.guest_entries['tc'].get(),
                    'name': self.guest_entries['name'].get(),
                    'surname': self.guest_entries['surname'].get(),
                    'email': self.guest_entries['email'].get(),
                    'phone': self.guest_entries['phone'].get(),
                    'birth_date': self.guest_entries['birth_date'].get_date(),
                    'gender': self.guest_entries['gender'].get()
                },
                "check_in": self.check_in_entry.get_date(),
                "check_out": self.check_out_entry.get_date(),
                "num_guests": self.guest_number_entry.get(),
                "room_info": {
                    "room_id": self.selected_room['room_id'],
                    "price": self.selected_room['price']
                },
                "dependents": dependents,
                "payment": {
                    "method": self.payment_method_combo.get(),
                    "amount": float(self.total_amount_label.cget("text").split()[1].replace("TL", "")),
                    "date": datetime.now().date()
                }
            }

            # Make the reservation using the database control function
            reservation_id = make_reservation(reservation_data)

            if reservation_id:
                messagebox.showinfo("Success", f"Reservation completed successfully! Reservation ID: {reservation_id}")
                self.main_menu()
            else:
                messagebox.showerror("Error", "An error occurred while making the reservation. Please try again.")

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")



    def cancel_reservation(self):
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
        info_window = tk.Toplevel(self.root)
        info_window.title("Get Reservation Info")
        info_window.geometry("400x300")

        tk.Label(info_window, text="Enter Reservation ID:").pack(pady=10)
        reservation_id_entry = tk.Entry(info_window)
        reservation_id_entry.pack(pady=5)

        tk.Label(info_window, text="Enter Guest TC:").pack(pady=10)
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