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

        tk.Label(reservation_window, text="Guest TC:").pack(pady=5)
        guest_tc_entry = tk.Entry(reservation_window)
        guest_tc_entry.pack(pady=5)

        tk.Label(reservation_window, text="Guest Name:").pack(pady=5)
        guest_name_entry = tk.Entry(reservation_window)
        guest_name_entry.pack(pady=5)

        tk.Label(reservation_window, text="Guest Surname:").pack(pady=5)
        guest_surname_entry = tk.Entry(reservation_window)
        guest_surname_entry.pack(pady=5)

        # Add dependents logic
        dependents = []

        def complete_reservation():
            # Collect reservation data
            reservation_data = {
                "main_guest": {
                    "tc": guest_tc_entry.get(),
                    "name": guest_name_entry.get(),
                    "surname": guest_surname_entry.get(),
                },
                "check_in": self.check_in_entry.get_date(),
                "check_out": self.check_out_entry.get_date(),
                "room_info": {
                    "room_id": self.selected_room["room_id"],
                    "price": self.selected_room["price"],
                },
                "dependents": dependents  # Ensure dependents are always included
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
        pass

    def get_reservation_info(self):
        # Get reservation info logic
        pass


def main():
    root = tk.Tk()
    app = HotelApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
