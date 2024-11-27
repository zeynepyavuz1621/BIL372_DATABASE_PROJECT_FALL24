import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from db_control_sql import get_filtered_hotels, make_reservation, fetch_reservation_details

class HotelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Reservation System")
        self.root.geometry("800x600")

        # Initialize variables
        self.hotels_window = None
        self.hotels_tree = None
        self.selected_room = None
        self.reservation_window = None
        self.dependent_entries = []

        self.setup_main_window()

    def setup_main_window(self):
        # Main search frame
        search_frame = ttk.LabelFrame(self.root, text="Search Hotels", padding=15)
        search_frame.pack(fill='x', padx=10, pady=5)

        # Dates
        dates_frame = ttk.Frame(search_frame)
        dates_frame.pack(fill='x', pady=5)

        ttk.Label(dates_frame, text="Check-in Date:").grid(row=0, column=0, padx=5, pady=5)
        self.check_in_entry = DateEntry(dates_frame, width=12, background='darkblue', 
                                        foreground='white', borderwidth=2)
        self.check_in_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(dates_frame, text="Check-out Date:").grid(row=0, column=2, padx=5, pady=5)
        self.check_out_entry = DateEntry(dates_frame, width=12, background='darkblue', 
                                        foreground='white', borderwidth=2)
        self.check_out_entry.grid(row=0, column=3, padx=5, pady=5)

        # Filters
        filters_frame = ttk.Frame(search_frame)
        filters_frame.pack(fill='x', pady=5)

        ttk.Label(filters_frame, text="Hotel Type:").grid(row=0, column=0, padx=5, pady=5)
        self.hotel_type_combo = ttk.Combobox(filters_frame, 
                                            values=['All', 'Lüks', 'İş', 'Resort', 'Butik', 'Ekonomik'],
                                            state='readonly', width=15)
        self.hotel_type_combo.grid(row=0, column=1, padx=5, pady=5)
        self.hotel_type_combo.set("All")

        ttk.Label(filters_frame, text="City:").grid(row=0, column=2, padx=5, pady=5)
        self.city_combo = ttk.Combobox(filters_frame, 
                                    values=['All', 'İstanbul', 'Antalya', 'İzmir', 'Muğla', 
                                            'Ankara', 'Bursa', 'Aydın', 'Mersin'],
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
        ttk.Button(search_frame, text="Search Hotels", 
                command=self.search_hotels).pack(pady=10)

        # Reservation Information Section
        reservation_frame = ttk.LabelFrame(self.root, text="Reservation Info", padding=15)
        reservation_frame.pack(fill='x', padx=10, pady=10)

        ttk.Label(reservation_frame, text="Reservation ID:").grid(row=0, column=0, padx=5, pady=5)
        self.reservation_id_entry = ttk.Entry(reservation_frame, width=15)
        self.reservation_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(reservation_frame, text="Customer TC:").grid(row=1, column=0, padx=5, pady=5)
        self.customer_name_entry = ttk.Entry(reservation_frame, width=20)
        self.customer_name_entry.grid(row=1, column=1, padx=5, pady=5)

        # Button to fetch reservation info
        ttk.Button(reservation_frame, text="Get Reservation Info", 
                command=self.get_reservation_info).grid(row=2, column=0, columnspan=2, pady=10)

        # Frame to display reservation details
        self.reservation_info_label = ttk.Label(reservation_frame, text="", justify="left")
        self.reservation_info_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def search_hotels(self):
        try:
            # Validate dates
            check_in = self.check_in_entry.get_date()
            check_out = self.check_out_entry.get_date()
            if check_out <= check_in:
                messagebox.showerror("Invalid Dates", 
                                   "Check-out date must be after check-in date")
                return

            # Validate price range
            price_min = float(self.price_min_entry.get()) if self.price_min_entry.get() else 0
            price_max = float(self.price_max_entry.get()) if self.price_max_entry.get() else float('inf')
            if price_max < price_min:
                messagebox.showerror("Invalid Price Range", 
                                   "Maximum price must be greater than minimum price")
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

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_hotel_results(self, hotels):
        if self.hotels_window:
            self.hotels_window.destroy()

        self.hotels_window = tk.Toplevel(self.root)
        self.hotels_window.title("Available Hotels")
        self.hotels_window.geometry("800x600")

        # Create Treeview with room_id column
        columns = ("Hotel Name", "Type", "Room Type", "Price per Night", "Room ID")
        self.hotels_tree = ttk.Treeview(self.hotels_window, columns=columns, show="headings", selectmode="browse")

        # Configure columns
        for col in columns:
            self.hotels_tree.heading(col, text=col)
            # Hide Room ID column
            if col == "Room ID":
                self.hotels_tree.column(col, width=0, stretch=False)
            else:
                width = 150 if col in ("Hotel Name", "Room Type") else 100
                self.hotels_tree.column(col, width=width)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.hotels_window, orient="vertical", 
                                 command=self.hotels_tree.yview)
        self.hotels_tree.configure(yscrollcommand=scrollbar.set)

        # Pack widgets
        self.hotels_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)

        # Insert data
        for hotel in hotels:
            values = list(hotel)  # Tüm değerleri alıyoruz
            self.hotels_tree.insert("", "end", values=values)

        # Bind selection event
        self.hotels_tree.bind("<<TreeviewSelect>>", self.on_hotel_select)

    def on_hotel_select(self, event):
        selection = self.hotels_tree.selection()
        if not selection:
            return

        item = self.hotels_tree.item(selection[0])
        values = item['values']
        
        # Make sure we have all required values
        if len(values) >= 5:
            self.selected_room = {
                'hotel_name': values[0],
                'hotel_type': values[1],
                'room_type': values[2],
                'price': float(values[3]),
                'room_id': values[4]
            }
            self.show_reservation_form()
        else:
            messagebox.showerror("Error", "Invalid room selection")

    def on_hotel_select(self, event):
        selection = self.hotels_tree.selection()
        if not selection:
            return

        item = self.hotels_tree.item(selection[0])
        # Seçilen otelin tüm bilgilerini alıyoruz
        self.selected_room = {
            'hotel_name': item['values'][0],
            'hotel_type': item['values'][1],
            'room_type': item['values'][2],
            'price': float(item['values'][3]),
            'room_id': item['values'][4]  # room_id'yi de ekliyoruz
        }
        self.show_reservation_form()


    def show_reservation_form(self):
        if self.reservation_window:
            self.reservation_window.destroy()

        self.reservation_window = tk.Toplevel(self.root)
        self.reservation_window.title("Make Reservation")
        self.reservation_window.geometry("800x800")

        # Create notebook for tabs
        notebook = ttk.Notebook(self.reservation_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)

        # Main guest tab
        main_frame = ttk.Frame(notebook)
        notebook.add(main_frame, text='Main Guest')

        # Dependents tab
        dependent_frame = ttk.Frame(notebook)
        notebook.add(dependent_frame, text='Dependents')

        # Hotel information
        hotel_frame = ttk.LabelFrame(main_frame, text="Selected Hotel")
        hotel_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(hotel_frame, text=f"Hotel: {self.selected_room['hotel_name']}").pack(pady=2)
        ttk.Label(hotel_frame, text=f"Room Type: {self.selected_room['room_type']}").pack(pady=2)
        ttk.Label(hotel_frame, text=f"Price per Night: {self.selected_room['price']} TL").pack(pady=2)

        # Main guest information
        guest_frame = ttk.LabelFrame(main_frame, text="Guest Information")
        guest_frame.pack(fill='x', padx=10, pady=5)

        # Guest fields
        self.guest_entries = {}
        guest_fields = [
            ('TC Number:', 'tc'),
            ('Name:', 'name'),
            ('Surname:', 'surname'),
            ('Email:', 'email'),
            ('Phone:', 'phone'),
            ('Birth Date:', 'birth_date'),
            ('Gender:', 'gender')
        ]

        for i, (label, field) in enumerate(guest_fields):
            ttk.Label(guest_frame, text=label).grid(row=i, column=0, padx=5, pady=2, sticky='e')
            
            if field == 'birth_date':
                self.guest_entries[field] = DateEntry(guest_frame, width=12)
            elif field == 'gender':
                self.guest_entries[field] = ttk.Combobox(guest_frame, values=['M', 'F'], 
                                                       state='readonly', width=15)
            else:
                self.guest_entries[field] = ttk.Entry(guest_frame, width=20)
            
            self.guest_entries[field].grid(row=i, column=1, padx=5, pady=2, sticky='w')


        # Dependents container
        self.dependents_container = ttk.Frame(dependent_frame)
        self.dependents_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        ttk.Button(dependent_frame, text="Add Dependent", 
                  command=self.add_dependent_form).pack(pady=5)

        # Payment information
        payment_frame = ttk.LabelFrame(self.reservation_window, text="Payment Information")
        payment_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(payment_frame, text="Payment Method:").pack(pady=2)
        self.payment_method = ttk.Combobox(payment_frame, 
                                         values= ['Kredi Kartı', 'Nakit', 'Banka Transferi', 'Online Ödeme'],
                                         state='readonly')
        self.payment_method.pack(pady=2)
        self.payment_method.set("Credit Card")

        # Total amount
        self.total_amount_label = ttk.Label(payment_frame, text="Total: 0 TL")
        self.total_amount_label.pack(pady=5)

        # Complete reservation button
        ttk.Button(self.reservation_window, text="Complete Reservation", 
                  command=self.complete_reservation).pack(pady=10)

        # Set up event bindings
        self.setup_event_bindings()
        # Calculate initial total
        self.update_total()

    def add_dependent_form(self):
        dependent_frame = ttk.LabelFrame(self.dependents_container, 
                                       text=f"Dependent {len(self.dependent_entries) + 1}")
        dependent_frame.pack(fill='x', pady=5)

        entries = {}
        fields = [
            ('TC Number:', 'tc'),
            ('Name:', 'name'),
            ('Last Name:','last_name'),
            ('Birth Date:', 'birth_date'),
            ('Gender:', 'gender'),
            ('Relation Type:', 'relation_type')
        ]

        for i, (label, field) in enumerate(fields):
            ttk.Label(dependent_frame, text=label).grid(row=i, column=0, padx=5, pady=2, sticky='e')
            
            if field == 'birth_date':
                entries[field] = DateEntry(dependent_frame, width=12)
            elif field == 'gender':
                entries[field] = ttk.Combobox(dependent_frame, values=['M', 'F'], 
                                            state='readonly', width=15)
            elif field == 'relation_type':
                entries[field] = ttk.Combobox(dependent_frame, values=['family', 'friend'], 
                                            state='readonly', width=15)
            else:
                entries[field] = ttk.Entry(dependent_frame, width=20)
            
            entries[field].grid(row=i, column=1, padx=5, pady=2, sticky='w')

        ttk.Button(dependent_frame, text="Remove", 
                  command=lambda: self.remove_dependent(dependent_frame)).grid(
                      row=len(fields), column=0, columnspan=2, pady=5)

        self.dependent_entries.append({
            'frame': dependent_frame,
            'entries': entries
        })
        
        self.update_total()

    def remove_dependent(self, frame_to_remove):
        self.dependent_entries = [entry for entry in self.dependent_entries 
                                if entry['frame'] != frame_to_remove]
        frame_to_remove.destroy()
        
        # Update numbering
        for i, entry in enumerate(self.dependent_entries):
            entry['frame'].configure(text=f"Dependent {i + 1}")
        
        self.update_total()

    def update_total(self, *args):
        try:
            check_in = self.check_in_entry.get_date()
            check_out = self.check_out_entry.get_date()
            num_nights = (check_out - check_in).days
            
            if num_nights <= 0:
                self.total_amount_label.configure(text="Total: 0 TL")
                return
            
            
            total = self.selected_room['price'] * num_nights * (len(self.dependent_entries)+1)
            
            self.total_amount_label.configure(text=f"Total: {total:.2f} TL")
            
        except Exception as e:
            print(f"Error calculating total: {e}")
            self.total_amount_label.configure(text="Total: 0 TL")

    def setup_event_bindings(self):
        self.check_in_entry.bind("<<DateEntrySelected>>", self.update_total)
        self.check_out_entry.bind("<<DateEntrySelected>>", self.update_total)

    def complete_reservation(self):
        try:
            # Validate main guest information
            if not all(entry.get() for entry in self.guest_entries.values()):
                messagebox.showerror("Error", "Please fill in all main guest information")
                return

            # Get dependents information
            dependents = []
            dep_num=0
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
                dep_num+=1

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
                "num_guests": dep_num+1,
                "room_info": {
                    "room_id": self.selected_room['room_id'],
                    "price": self.selected_room['price']
                },
                "dependents": dependents,
                "payment": {
                    "method": self.payment_method.get(),
                    "amount": float(self.total_amount_label.cget("text").split()[1].replace("TL", "")),
                    "date": datetime.now().date()
                }
            }

            # Make reservation
            success = make_reservation(reservation_data)
            
            if success:
                messagebox.showinfo("Success", "Reservation completed successfully!\nYour reservation number:\t" + (str)(success))
                self.reservation_window.destroy()
                if self.hotels_window:
                    self.hotels_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to complete reservation")

        except Exception as e:
            messagebox.showerror("Error", f"Error completing reservation: {str(e)}")


    def get_reservation_info(self):
        # Retrieve the reservation ID and customer name
        reservation_id = self.reservation_id_entry.get()
        customer_name = self.customer_name_entry.get()

        # Check if both fields are filled
        if reservation_id and customer_name:
            # Simulate fetching reservation details (this could be a database call or API request)
            reservation_info = fetch_reservation_details(reservation_id, customer_name)
            
            # Display the reservation details
            if reservation_info:
                if reservation_info['is_canceled']:
                    flag = "Canceled"
                else:
                    flag = "Active"
                reservation_text = f"Reservation ID: {reservation_info['reservation_id']}\n"
                reservation_text += f"Reservation Status: {flag}\n\n"
                reservation_text += f"Customer Name: {reservation_info['guest_name']}\n"
                reservation_text += f"Customer Surname: {reservation_info['guest_surname']}\n\n"
                reservation_text += f"Hotel Name: {reservation_info['hotel_name']}\n\n"
                reservation_text += f"Check-in Date: {reservation_info['check_in']}\n"
                reservation_text += f"Check-out Date: {reservation_info['check_out']}\n"
                reservation_text += f"Price: {reservation_info['price_per_night']} TL"
                self.reservation_info_label.config(text=reservation_text)
            else:
                self.reservation_info_label.config(text="No reservation found with this ID and name.")
        else:
            self.reservation_info_label.config(text="Please enter both Reservation ID and Customer Name.")



def main():
    root = tk.Tk()
    app = HotelApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()