import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import json
import os
from db_control_sql import get_filtered_hotels, make_reservation, fetch_reservation_details, get_hotel_photos,cancel_reservation,make_comment_in_db,get_comments,get_room_photos

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏨 Hotel Reservation System")
        self.root.geometry("1200x800")
        
        # Configure modern style
        self.setup_styles()

        # Create container
        self.container = ttk.Frame(root)
        self.container.pack(side="top", fill="both", expand=True)

        # Dictionary to store frames
        self.frames = {}
        
        # Initialize all frames
        for F in (SearchPage, HotelsPage, ReservationPage,AddCommentPage):
            frame = F(self.container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Configure container grid
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Show initial frame
        self.show_frame("SearchPage")

        # Shared data between frames
        self.selected_room = None
        self.search_criteria = None
    def setup_styles(self):
        # Color scheme (Airbnb-inspired)
        COLORS = {
            'primary': '#FF5A5F',       # Airbnb red
            'secondary': '#00A699',     # Teal
            'background': '#FFFFFF',    # White
            'text': '#484848',         # Dark gray
            'light_gray': '#767676',   # Light gray
            'super_light': '#F7F7F7'   # Almost white
        }

        style = ttk.Style()
        style.configure('TFrame', background=COLORS['background'])
        style.configure('TLabel', 
                       background=COLORS['background'],
                       foreground=COLORS['text'],
                       font=('Helvetica', 11))
        style.configure('TLabelframe', 
                       background=COLORS['background'],
                       foreground=COLORS['text'])
        style.configure('TLabelframe.Label', 
                       font=('Helvetica', 12, 'bold'),
                       background=COLORS['background'],
                       foreground=COLORS['text'])
        
        # Custom button style
        style.configure('Accent.TButton',
                       background=COLORS['primary'],
                       foreground='white',
                       padding=(20, 10),
                       font=('Helvetica', 11, 'bold'))
        
        # Entry style
        style.configure('TEntry',
                       fieldbackground=COLORS['super_light'],
                       padding=5)
        
        # Combobox style
        style.configure('TCombobox',
                       background=COLORS['super_light'],
                       padding=5)
        
        # Hotel card style
        style.configure('HotelCard.TFrame',
                       background=COLORS['background'],
                       relief='solid',
                       borderwidth=1)

        return COLORS

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

    def start_new_search(self):
        self.selected_room = None
        self.search_criteria = None
        self.show_frame("SearchPage")

class SearchPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Main container for better organization
        main_container = ttk.Frame(self)
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left side: Search section
        left_frame = ttk.Frame(main_container)
        left_frame.pack(side='left', fill='both', expand=True, padx=10)
        
        # Header
        header_label = ttk.Label(left_frame, 
                            text="🏨 Find Your Perfect Stay",
                            font=('Helvetica', 24, 'bold'))
        header_label.pack(pady=10)
        
        # Search section
        search_frame = ttk.LabelFrame(left_frame, text="🔍 Search Hotels", padding=20)
        search_frame.pack(fill='x', pady=5)

        # Dates with modern calendar styling
        dates_frame = ttk.Frame(search_frame)
        dates_frame.pack(fill='x', pady=10)

        date_style = {'background': '#FF5A5F',
                     'foreground': 'white',
                     'borderwidth': 0,
                     'font': ('Helvetica', 10),
                     'selectbackground': '#00A699'}

        ttk.Label(dates_frame, 
                 text="Check-in Date:",
                 font=('Helvetica', 11, 'bold')).grid(row=0, column=0, padx=5, pady=5)
        self.check_in_entry = DateEntry(dates_frame, width=15, **date_style)
        self.check_in_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(dates_frame,
                 text="Check-out Date:",
                 font=('Helvetica', 11, 'bold')).grid(row=0, column=2, padx=5, pady=5)
        self.check_out_entry = DateEntry(dates_frame, width=15, **date_style)
        self.check_out_entry.grid(row=0, column=3, padx=5, pady=5)

        # Filters with modern styling
        filters_frame = ttk.Frame(search_frame)
        filters_frame.pack(fill='x', pady=10)

        ttk.Label(filters_frame,
                 text="Hotel Type:",
                 font=('Helvetica', 11, 'bold')).grid(row=0, column=0, padx=5, pady=5)
        self.hotel_type_combo = ttk.Combobox(filters_frame, 
                                           values=['All', 'Lüks', 'İş', 'Resort', 'Butik', 'Ekonomik'],
                                           state='readonly', width=15)
        self.hotel_type_combo.grid(row=0, column=1, padx=5, pady=5)
        self.hotel_type_combo.set("All")

        ttk.Label(filters_frame,
                 text="City:",
                 font=('Helvetica', 11, 'bold')).grid(row=0, column=2, padx=5, pady=5)
        self.city_combo = ttk.Combobox(filters_frame, 
                                     values=["Dubai", "Miami", "Cancun", "Bali", "Phuket", 
                                            "Barcelona", "Maldives", "Hawaii", "Nice", "Gold Coast"],
                                     state='readonly', width=15)
        self.city_combo.grid(row=0, column=3, padx=5, pady=5)
        self.city_combo.set("All")

        # Price range with modern styling
        price_frame = ttk.Frame(search_frame)
        price_frame.pack(fill='x', pady=10)

        ttk.Label(price_frame,
                 text="Price Range (TL):",
                 font=('Helvetica', 11, 'bold')).pack(side='left', padx=5)
        self.price_min_entry = ttk.Entry(price_frame, width=10)
        self.price_min_entry.pack(side='left', padx=5)
        ttk.Label(price_frame, text="-",
                 font=('Helvetica', 11, 'bold')).pack(side='left')
        self.price_max_entry = ttk.Entry(price_frame, width=10)
        self.price_max_entry.pack(side='left', padx=5)

        # Search button with Airbnb styling
        search_button = tk.Button(search_frame,
                                text="Search Hotels",
                                command=self.search_hotels,
                                font=('Helvetica', 12, 'bold'),
                                bg='#FF5A5F',
                                fg='white',
                                padx=30,
                                pady=10,
                                relief='flat',
                                cursor='hand2')
        search_button.pack(pady=20)

        # Add Reservation Info Section
        info_frame = ttk.Frame(main_container)
        info_frame.pack(side='left', fill='both', expand=True, padx=10)
        
        self.setup_reservation_info(info_frame)
        self.setup_cancel_info(info_frame)

    def setup_reservation_info(self,parent):
        reservation_frame = ttk.LabelFrame(parent, text="📋 Reservation Info", padding=20)
        reservation_frame.pack(fill='x', pady=5)

        grid_frame = ttk.Frame(reservation_frame)
        grid_frame.pack(fill='x', pady=5)

        # Reservation Info
        info_frame = ttk.Frame(grid_frame)
        info_frame.pack(side='left', fill='both', expand=True)

        # Reservation ID field
        ttk.Label(info_frame, text="Reservation ID:", font=('Helvetica', 11, 'bold'), foreground='#484848').pack(pady=(0, 5))
        self.reservation_id_entry = ttk.Entry(info_frame, width=20, font=('Helvetica', 10))
        self.reservation_id_entry.pack(pady=(0, 10))

        # Guest TC field
        ttk.Label(info_frame, text="Guest TC:", font=('Helvetica', 11, 'bold'), foreground='#484848').pack(pady=(0, 5))
        self.guest_id_entry = ttk.Entry(info_frame, width=20, font=('Helvetica', 10))
        self.guest_id_entry.pack(pady=(0, 10))

        # Get Info button
        info_button = tk.Button(info_frame, text="Get Reservation Info", command=self.get_reservation_info,
                            font=('Helvetica', 11, 'bold'), bg='#00A699', fg='white',
                            padx=20, pady=8, relief='flat', cursor='hand2')
        info_button.pack(pady=10)


        # Info display label
        self.reservation_info_label = ttk.Label(reservation_frame, text="", justify="left",
                                            font=('Helvetica', 11), wraplength=400)
        self.reservation_info_label.pack(pady=10)


    def setup_cancel_info(self,parent):
        cancel_frame = ttk.LabelFrame(parent, text="❌ Cancel Reservation", padding=20)
        cancel_frame.pack(fill='x', pady=5)

        # Reservation ID, Guest TC, and Cancel button
        input_frame = ttk.Frame(cancel_frame)
        input_frame.pack(fill='x', pady=5)

        ttk.Label(
            input_frame,
            text="Reservation ID:",
            font=('Helvetica', 11, 'bold'),
            foreground='#484848'
        ).pack(pady=(0, 5))
        
        self.reservation_id_entry = ttk.Entry(
            input_frame,
            width=20,
            font=('Helvetica', 10)
        )
        self.reservation_id_entry.pack(pady=(0, 10))

        ttk.Label(
            input_frame,
            text="Guest TC:",
            font=('Helvetica', 11, 'bold'),
            foreground='#484848'
        ).pack(pady=(0, 5))
        
        self.guest_id_entry = ttk.Entry(
            input_frame,
            width=20,
            font=('Helvetica', 10)
        )
        self.guest_id_entry.pack(pady=(0, 10))

        cancel_button = tk.Button(
            input_frame,
            text="Cancel Reservation",
            command=self.cancel_reservation,
            font=('Helvetica', 11, 'bold'),
            bg='#FF5A5F',
            fg='white',
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        cancel_button.pack(pady=10)

        self.cancel_result_label = ttk.Label(
            cancel_frame,
            text="",
            justify="left",
            font=('Helvetica', 11),
            wraplength=400
        )
        self.cancel_result_label.pack(pady=10)

    def cancel_reservation(self):
        reservation_id = self.reservation_id_entry.get()
        guest_id = self.guest_id_entry.get()

        if reservation_id and guest_id:
            result = cancel_reservation(reservation_id, guest_id)
            if result["success"]:
                self.cancel_result_label.configure(text=result["message"], foreground='green')
            else:
                self.cancel_result_label.configure(text=result["message"], foreground='red')
        else:
            self.cancel_result_label.configure(text="Please enter both Reservation ID and Guest ID",foreground="red")
        

    def search_hotels(self):
        try:
            # Get and validate search criteria
            check_in = self.check_in_entry.get_date()
            check_out = self.check_out_entry.get_date()
            
            if check_out <= check_in:
                messagebox.showerror("Invalid Dates", 
                                   "Check-out date must be after check-in date")
                return

            price_min = float(self.price_min_entry.get()) if self.price_min_entry.get() else 0
            price_max = float(self.price_max_entry.get()) if self.price_max_entry.get() else float('inf')
            
            if price_max < price_min:
                messagebox.showerror("Invalid Price Range", 
                                   "Maximum price must be greater than minimum price")
                return

            # Store search criteria in controller
            self.controller.search_criteria = {
                'check_in': check_in,
                'check_out': check_out,
                'hotel_type': self.hotel_type_combo.get(),
                'city': self.city_combo.get(),
                'price_min': price_min,
                'price_max': price_max
            }

            # Get hotels and pass to hotels page
            hotels = get_filtered_hotels(**self.controller.search_criteria)
            
            if not hotels:
                messagebox.showinfo("No Results", "No hotels found matching your criteria")
                return

            # Update hotels page and show it
            hotels_page = self.controller.frames["HotelsPage"]
            hotels_page.display_hotels(hotels)
            self.controller.show_frame("HotelsPage")

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def get_reservation_info(self):
        reservation_id = self.reservation_id_entry.get()
        guest_id = self.guest_id_entry.get()

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
    


class HotelsPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.photo_references = []
        
        # Create header with back button
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(header_frame, text="← Back to Search",
                  command=lambda: controller.show_frame("SearchPage")).pack(side="left")
        
        # Create scrollable frame for hotels
        self.setup_scrollable_frame()

    def setup_scrollable_frame(self):
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self, background="#f0f8ff")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", 
                                     command=self.canvas.yview)
        
        # Create the scrollable frame
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        # Configure the canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Create window in canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack everything
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Add mousewheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def display_hotels(self, hotels):
    # Clear existing content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.photo_references = []
        
        # Get hotel photos
        hotel_photos = get_hotel_photos()
        photo_dict = {photo[1]: photo[2] for photo in hotel_photos}
        
        # Configure grid
        self.scrollable_frame.grid_columnconfigure((0,1,2), weight=1, uniform="column")
        
        # Calculate card width based on window width
        card_width = 350  # Fixed width for each card
        
        row = col = 0
        max_columns = 3
        
        project_root = os.path.dirname(os.path.abspath(__file__))
        
        for hotel in hotels:
            # Create card frame with fixed width and padding
            card = ttk.Frame(self.scrollable_frame, style='Card.TFrame')
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            try:
                hotel_id = hotel[0]
                
                # Add hotel image first
                self.add_hotel_image(card, hotel_id, photo_dict, project_root, card_width)
                
                # Create info section with padding
                info_frame = ttk.Frame(card, style='CardInfo.TFrame')
                info_frame.pack(fill="x", padx=15, pady=(10,15))
                
                # Hotel name and type in header
                name_frame = ttk.Frame(info_frame)
                name_frame.pack(fill="x", pady=5)
                
                hotel_name = ttk.Label(name_frame, 
                                    text=hotel[1],
                                    font=('Helvetica', 16, 'bold'),
                                    foreground='#484848')
                hotel_name.pack(side="left")
                
                ttk.Label(name_frame, 
                        text=" • ",
                        font=('Helvetica', 16)).pack(side="left")
                
                ttk.Label(name_frame, 
                        text=hotel[2],
                        font=('Helvetica', 14),
                        foreground='#717171').pack(side="left")
                
                # Room information
                ttk.Label(info_frame, 
                        text=f"Room Type: {hotel[3]}", 
                        font=('Helvetica', 12),
                        foreground='#717171').pack(fill="x", pady=5)
                
                # Price section
                price_frame = ttk.Frame(info_frame)
                price_frame.pack(fill="x", pady=5)
                
                price_label = ttk.Label(price_frame, 
                                    text=f"{hotel[4]} TL",
                                    font=('Helvetica', 18, 'bold'),
                                    foreground='#484848')
                price_label.pack(side="left")
                
                ttk.Label(price_frame, 
                        text=" per night",
                        font=('Helvetica', 12),
                        foreground='#717171').pack(side="left", padx=5, pady=3)
                button_frame = ttk.Frame(info_frame)
                button_frame.pack(fill="x", pady=(10,0))
                
                # Book button with hover effect
                book_button = tk.Button(button_frame, 
                                    text="Book Now",
                                    command=lambda h=hotel: self.select_hotel(h),
                                    font=('Helvetica', 12, 'bold'),
                                    bg='#FF5A5F',
                                    fg='white',
                                    activebackground='#FF4449',
                                    activeforeground='white',
                                    padx=25,
                                    pady=8,
                                    relief="flat",
                                    cursor="hand2")
                book_button.pack(pady=(10,0))

                comment_button = tk.Button(button_frame,
                                    text="Add Comment",
                                    command=lambda h=hotel: self.show_comment_page(h),
                                    font=('Helvetica', 12, 'bold'),
                                    bg='#00A699',
                                    fg='white',
                                    activebackground='#009688',
                                    activeforeground='white',
                                    padx=15,
                                    pady=8,
                                    relief="flat",
                                    cursor="hand2")
                comment_button.pack(padx=5)
                
                # Update grid position
                col += 1
                if col >= max_columns:
                    col = 0
                    row += 1
                    
            except Exception as e:
                print(f"Error creating hotel card: {e}")

    def create_hotel_card(self, hotel, photo_dict, project_root, row, col):
        # Create card frame
        card = ttk.Frame(self.scrollable_frame, style='HotelCard.TFrame')
        card.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
        
        try:
            hotel_id = hotel[0]
            
            # Create info section
            info_frame = ttk.Frame(card)
            info_frame.pack(fill="x", padx=15, pady=10)
            
            # Hotel name and type section
            name_frame = ttk.Frame(info_frame)
            name_frame.pack(fill="x", pady=5)
            
            ttk.Label(name_frame, text=hotel[1], 
                     font=("Helvetica", 16, "bold")).pack(side="left", pady=2)
            ttk.Label(name_frame, text=" • ",
                     font=("Helvetica", 14)).pack(side="left")
            ttk.Label(name_frame, text=hotel[2],
                     font=("Helvetica", 14)).pack(side="left")
            
            # Room information
            ttk.Label(info_frame, text=f"Room Type: {hotel[3]}", 
                     font=("Helvetica", 12)).pack(fill="x", pady=5)
            
            # Price section
            price_frame = ttk.Frame(info_frame)
            price_frame.pack(fill="x", pady=5)
            ttk.Label(price_frame, text=f"{hotel[4]} TL",
                     font=("Helvetica", 16, "bold")).pack(side="left")
            ttk.Label(price_frame, text=" per night",
                     font=("Helvetica", 10)).pack(side="left", padx=5)
            
            
            
            # Add book button
            tk.Button(info_frame, text="Book Now",
                     command=lambda h=hotel: self.select_hotel(h),
                     font=("Helvetica", 10, "bold"),
                     bg='#2c3e50', fg='white',
                     padx=20, pady=5,
                     relief="flat",
                     cursor="hand2").pack(pady=10)
            
            
            # Add hotel image
            self.add_hotel_image(card, hotel_id, photo_dict, project_root)
            
        except Exception as e:
            print(f"Error creating hotel card: {e}")
    def show_comment_page(self, hotel):
        """Navigate to comment page and store selected hotel info"""
        if len(hotel) >= 5:
            self.controller.selected_room = {
                'hotel_id': hotel[0],
                'hotel_name': hotel[1],
                'hotel_type': hotel[2],
                'room_type': hotel[3],
                'price': float(hotel[4]),
                'room_id': hotel[5]
            }
            self.controller.show_frame("AddCommentPage")

    def add_hotel_image(self, card, hotel_id, photo_dict, project_root, card_width):
        if hotel_id in photo_dict:
            image_path = photo_dict[hotel_id]
            full_path = os.path.normpath(os.path.join(project_root, image_path))
            try:
                if os.path.exists(full_path):
                    image = Image.open(full_path)
                    # Calculate height based on aspect ratio
                    aspect_ratio = 0.75  # 4:3 aspect ratio
                    card_height = int(card_width * aspect_ratio)
                    image = image.resize((card_width, card_height), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    self.photo_references.append(photo)
                    
                    image_frame = ttk.Frame(card)
                    image_frame.pack(fill="x")
                    
                    image_label = ttk.Label(image_frame, image=photo)
                    image_label.pack()
                else:
                    self.add_placeholder_image(card, card_width)
            except Exception as img_error:
                print(f"Error loading image: {img_error}")
                self.add_placeholder_image(card, card_width)
        else:
            self.add_placeholder_image(card, card_width)

    def add_placeholder_image(self, card, card_width):
        placeholder_frame = ttk.Frame(card, style='Placeholder.TFrame')
        placeholder_frame.pack(fill="x", pady=10)

        # Aspect ratio and placeholder height
        aspect_ratio = 0.75
        card_height = int(card_width * aspect_ratio)

        # Placeholder label
        placeholder_label = ttk.Label(
            placeholder_frame,
            text="Image not available",
            font=('Helvetica', 12, 'italic'),
            foreground='#717171',
            anchor='center',
            justify='center'
        )
        placeholder_label.pack(fill="both", expand=True, pady=(card_height // 4))

    def select_hotel(self, hotel):
        if len(hotel) >= 5:
            self.controller.selected_room = {
                'hotel_id': hotel[0],  # Add hotel_id
                'hotel_name': hotel[1],
                'hotel_type': hotel[2],
                'room_type': hotel[3],
                'price': float(hotel[4]),
                'room_id': hotel[5]
        }
            # Get ReservationPage instance and update it before showing
            reservation_page = self.controller.frames["ReservationPage"]
            self.controller.show_frame("ReservationPage")
            reservation_page.update_hotel_info()

class ReservationPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.dependent_entries = []
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        
        # Create header with back button
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(header_frame, text="← Back to Hotels",
                  command=lambda: controller.show_frame("HotelsPage")).pack(side="left")

        # Create main scrollable canvas
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # Create main container for all content
        self.main_container = ttk.Frame(self.canvas)
        
        # Configure the canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack scrollbar and canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create window in canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.main_container, anchor="nw")
        
        # Bind events for scrolling
        self.main_container.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.bind_mouse_wheel()
        
        # Create notebook for tabs in the main container
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)

        # Create frames for tabs
        self.setup_main_guest_tab()
        self.setup_dependents_tab()
        
        # Payment section
        self.setup_payment_section()
        
        # Comment section
        self.setup_comment_section()
       # self.hotel_image_frame = ttk.Frame(self.main_container)
        #self.hotel_image_frame.pack(fill='x', padx=10, pady=10)

    def on_frame_configure(self, event=None):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """When canvas is resized, resize the inner frame to match"""
        min_width = self.main_container.winfo_reqwidth()
        if event.width > min_width:
            # Update the width of the canvas window to fill the canvas
            self.canvas.itemconfig(self.canvas_window, width=event.width)

    def bind_mouse_wheel(self):
        """Bind mouse wheel to scrolling"""
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        # Bind mouse wheel to the canvas
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def setup_main_guest_tab(self):
        main_frame = ttk.Frame(self.notebook)
        self.notebook.add(main_frame, text='Main Guest')

        # Hotel information
        hotel_frame = ttk.LabelFrame(main_frame, text="Selected Hotel")
        hotel_frame.pack(fill='x', padx=10, pady=5)

        # Hotel info labels will be updated when showing the form
        self.hotel_name_label = ttk.Label(hotel_frame, text="", font=('Helvetica', 14, 'bold'))
        self.hotel_name_label.pack(pady=3)
        self.room_type_label = ttk.Label(hotel_frame, text="", font=('Helvetica', 12))
        self.room_type_label.pack(pady=3)
        self.price_label = ttk.Label(hotel_frame, text="", font=('Helvetica', 13, 'bold'))
        self.price_label.pack(pady=3)

        # Guest information
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

    def setup_dependents_tab(self):
        dependent_frame = ttk.Frame(self.notebook)
        self.notebook.add(dependent_frame, text='Dependents')

        self.dependents_container = ttk.Frame(dependent_frame)
        self.dependents_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Add Dependent button with Airbnb styling
        add_button = tk.Button(
            dependent_frame,
            text="+ Add Dependent",
            command=self.add_dependent_form,
            font=('Helvetica', 11, 'bold'),
            bg='#FF5A5F',
            fg='white',
            activebackground='#FF4449',
            activeforeground='white',
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        add_button.pack(pady=10)

    def setup_payment_section(self):
        payment_frame = ttk.LabelFrame(self, text="Payment Information", padding=15)
        payment_frame.pack(fill='x', padx=20, pady=10)

        # Payment method with better layout
        method_frame = ttk.Frame(payment_frame)
        method_frame.pack(fill='x', pady=5)
        
        ttk.Label(
            method_frame,
            text="Payment Method:",
            font=('Helvetica', 11, 'bold'),
            foreground='#484848'
        ).pack(side='left', padx=5)
        
        self.payment_method = ttk.Combobox(
            method_frame,
            values=['Kredi Kartı', 'Nakit', 'Banka Transferi', 'Online Ödeme'],
            state='readonly',
            width=20,
            font=('Helvetica', 10)
        )
        self.payment_method.pack(side='left', padx=5)
        self.payment_method.set('Kredi Kartı')

        # Total amount with prominent styling
        self.total_amount_label = ttk.Label(
            payment_frame,
            text="Total: 0 TL",
            font=('Helvetica', 16, 'bold'),
            foreground='#FF5A5F'
        )
        self.total_amount_label.pack(pady=10)

        # Complete reservation button with Airbnb styling
        complete_button = tk.Button(
            self,
            text="Complete Reservation",
            command=self.complete_reservation,
            font=('Helvetica', 12, 'bold'),
            bg='#FF5A5F',
            fg='white',
            activebackground='#FF4449',
            activeforeground='white',
            padx=30,
            pady=10,
            relief='flat',
            cursor='hand2'
        )
        complete_button.pack(pady=15)
    def setup_comment_section(self):
        """Set up the comment section to display only."""
        comment_frame = ttk.LabelFrame(self.main_container, text="💬 Hotel Reviews & Comments", padding=15)
        comment_frame.pack(fill='x', padx=20, pady=10)

        # Comments display area
        self.comments_display = tk.Text(comment_frame, height=6, width=50, state='disabled')
        self.comments_display.pack(pady=10, fill='x')

        # Refresh button
        refresh_button = tk.Button(
            comment_frame,
            text="Refresh Comments",
            command=self.load_comments,
            font=('Helvetica', 11, 'bold'),
            bg='#00A699',
            fg='white',
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        refresh_button.pack(pady=5)

    def load_comments(self):
        if not self.controller.selected_room:
            return

        hotel_name = self.controller.selected_room['hotel_name']
        hotel_id = self.controller.selected_room['hotel_id']  # Now we can use this directly
        
        comments = get_comments(hotel_id)
        
        # Enable text widget for updating
        self.comments_display.config(state='normal')
        self.comments_display.delete(1.0, tk.END)
        
        # Display header
        self.comments_display.insert(tk.END, f"Comments for {hotel_name}:\n\n")
        
        # Display each comment
        if comments:
            for comment in comments:
                # Add stars based on rating
                stars = "⭐" * comment['rating']
                
                # Format the comment text
                comment_text = f"{stars}\n"
                comment_text += f"By {comment['guest_name']} on {comment['date']}\n"
                comment_text += f"{comment['text']}\n"
                comment_text += "─" * 50 + "\n\n"
                
                self.comments_display.insert(tk.END, comment_text)
        else:
            self.comments_display.insert(tk.END, "No comments yet for this hotel.\n")
        
        self.comments_display.config(state='disabled')

    def update_hotel_info(self):
        if self.controller.selected_room:
            # Add styling to make it more prominent
            self.hotel_name_label.config(
                text=f"Hotel: {self.controller.selected_room['hotel_name']}",
                font=('Helvetica', 12, 'bold'),
                foreground='#484848'
            )
            self.room_type_label.config(
                text=f"Room Type: {self.controller.selected_room['room_type']}",
                font=('Helvetica', 11),
                foreground='#717171'
            )
            self.price_label.config(
                text=f"Price per Night: {self.controller.selected_room['price']} TL",
                font=('Helvetica', 12, 'bold'),
                foreground='#FF5A5F'
            )
            self.load_comments()
            self.update_total()
            #self.setup_room_info()
            #self.setup_room_image()
        else:
            # Clear labels if no room is selected
            self.hotel_name_label.config(text="")
            self.room_type_label.config(text="")
            self.price_label.config(text="")

    def add_dependent_form(self):
        dependent_frame = ttk.LabelFrame(self.dependents_container, 
                                       text=f"Dependent {len(self.dependent_entries) + 1}")
        dependent_frame.pack(fill='x', pady=5)

        entries = {}
        fields = [
            ('TC Number:', 'tc'),
            ('Name:', 'name'),
            ('Last Name:', 'last_name'),
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
            if not self.controller.search_criteria or not self.controller.selected_room:
                return

            check_in = self.controller.search_criteria['check_in']
            check_out = self.controller.search_criteria['check_out']
            num_nights = (check_out - check_in).days
            
            if num_nights <= 0:
                self.total_amount_label.configure(text="Total: 0 TL")
                return
            
            total = self.controller.selected_room['price'] * num_nights * (len(self.dependent_entries) + 1)
            self.total_amount_label.configure(text=f"Total: {total:.2f} TL")
            
        except Exception as e:
            print(f"Error calculating total: {e}")
            self.total_amount_label.configure(text="Total: 0 TL")

    def complete_reservation(self):
        try:
            if not self.controller.selected_room:
                messagebox.showerror("Error", "No room selected")
                return

            # Validate main guest information
            if not all(entry.get() for entry in self.guest_entries.values()):
                messagebox.showerror("Error", "Please fill in all main guest information")
                return

            # Get dependents information
            dependents = []
            dep_num = 0
            for dep in self.dependent_entries:
                if not all(entry.get() for entry in dep['entries'].values()):
                    messagebox.showerror("Error", 
                                       "Please fill in all dependent information or remove incomplete dependents")
                    return
                    
                dependent_data = {
                    'tc': dep['entries']['tc'].get(),
                    'name': dep['entries']['name'].get(),
                    'birth_date': dep['entries']['birth_date'].get_date(),
                    'gender': dep['entries']['gender'].get(),
                    'relation_type': dep['entries']['relation_type'].get()
                }
                dependents.append(dependent_data)
                dep_num += 1

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
                "check_in": self.controller.search_criteria['check_in'],
                "check_out": self.controller.search_criteria['check_out'],
                "num_guests": dep_num + 1,
                "room_info": self.controller.selected_room,
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
                messagebox.showinfo("Success", 
                                  f"Reservation completed successfully!\nYour reservation number: {success}")
                self.controller.start_new_search()
            else:
                messagebox.showerror("Error", "Failed to complete reservation")

        except Exception as e:
            messagebox.showerror("Error", f"Error completing reservation: {str(e)}")
    def setup_room_info(self):
        # Add styling to make it more prominent
        self.hotel_name_label.config(
            text=f"Hotel: {self.controller.selected_room['hotel_name']}",
            font=('Helvetica', 12, 'bold'),
            foreground='#484848'
        )
        self.room_type_label.config(
            text=f"Room Type: {self.controller.selected_room['room_type']}",
            font=('Helvetica', 11),
            foreground='#717171'
        )
        self.price_label.config(
            text=f"Price per Night: {self.controller.selected_room['price']} TL",
            font=('Helvetica', 12, 'bold'),
            foreground='#FF5A5F'
        )
    '''
    def setup_room_image(self):
        # Clear any existing image
        for widget in self.hotel_image_frame.winfo_children():
            widget.destroy()

        if self.controller.selected_room:
            hotel_id = self.controller.selected_room['hotel_id']
            room_id = self.controller.selected_room['room_id']

            room_photos = get_room_photos(hotel_id)
            print(room_photos)
            if room_photos:
                image_path = room_photos[0][1]
                print(image_path)
                full_path = os.path.normpath(os.path.join(self.project_root, image_path))
                try:
                    if os.path.exists(full_path):
                        image = Image.open(full_path)
                        # Resize the image to fit the frame
                        image = image.resize((400, 300), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(image)
                        self.photo_reference = photo
                        image_label = ttk.Label(self.hotel_image_frame, image=photo)
                        image_label.pack(pady=10)
                    else:
                        self.add_placeholder_image()
                except Exception as img_error:
                    print(f"Error loading image: {img_error}")
                    self.add_placeholder_image()
            else:
                self.add_placeholder_image()
        else:
            self.add_placeholder_image()

    def add_placeholder_image(self):
        # Clear any existing image
        for widget in self.hotel_image_frame.winfo_children():
            widget.destroy()

        placeholder_label = ttk.Label(
            self.hotel_image_frame,
            text="Image not available",
            font=('Helvetica', 12, 'italic'),
            foreground='#717171',
            anchor='center',
            justify='center'
        )
        placeholder_label.pack(pady=10)
     ''' 


class AddCommentPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Header with back button
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(
            header_frame,
            text="← Back to Hotels",
            command=lambda: controller.show_frame("HotelsPage")
        ).pack(side="left")

        # Main content frame
        content_frame = ttk.LabelFrame(
            self,
            text="✍️ Add Your Review",
            padding=20
        )
        content_frame.pack(fill='x', padx=20, pady=10)

        # Guest Verification Frame
        verify_frame = ttk.LabelFrame(content_frame, text="Guest Information", padding=10)
        verify_frame.pack(fill='x', pady=5)

        # Guest TC field
        tc_frame = ttk.Frame(verify_frame)
        tc_frame.pack(fill='x', pady=2)
        ttk.Label(tc_frame, text="TC Number:").pack(side='left', padx=5)
        self.comment_tc_entry = ttk.Entry(tc_frame, width=20)
        self.comment_tc_entry.pack(side='left', padx=5)

        # Reservation ID field
        res_frame = ttk.Frame(verify_frame)
        res_frame.pack(fill='x', pady=2)
        ttk.Label(res_frame, text="Reservation ID:").pack(side='left', padx=5)
        self.reservation_id_entry = ttk.Entry(res_frame, width=20)
        self.reservation_id_entry.pack(side='left', padx=5)

        # Rating selection
        rating_frame = ttk.Frame(content_frame)
        rating_frame.pack(fill='x', pady=10)
        
        ttk.Label(rating_frame, text="Rating:").pack(side='left', padx=5)
        self.rating_var = tk.StringVar(value="5")
        self.rating_combo = ttk.Combobox(
            rating_frame,
            textvariable=self.rating_var,
            values=["1", "2", "3", "4", "5"],
            state="readonly",
            width=5
        )
        self.rating_combo.pack(side='left', padx=5)

        # Comment text area
        ttk.Label(content_frame, text="Your Comment:").pack(anchor='w', pady=(5,0))
        self.comment_text = tk.Text(content_frame, height=4, width=50)
        self.comment_text.pack(pady=5, fill='x')

        # Submit button
        submit_button = tk.Button(
            content_frame,
            text="Submit Review",
            command=self.submit_comment,
            font=('Helvetica', 11, 'bold'),
            bg='#FF5A5F',
            fg='white',
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        submit_button.pack(pady=10)

    def submit_comment(self):
        """Submit a new comment"""
        if not self.controller.selected_room:
            messagebox.showerror("Error", "No hotel selected")
            return

        comment_content = self.comment_text.get("1.0", tk.END).strip()
        num_stars = int(self.rating_var.get())

        if not comment_content:
            messagebox.showerror("Error", "Please enter a comment")
            return

        guest_tc = self.comment_tc_entry.get().strip()
        hotel_name = self.controller.selected_room['hotel_name']
        current_date = datetime.now().date()

        result = make_comment_in_db(
            current_date=current_date,
            hotel_name=hotel_name,
            guest_tc=guest_tc,
            comment=comment_content,
            rating=num_stars
        )

        if result['success']:
            messagebox.showinfo("Success", "Comment added successfully!")
            self.comment_text.delete("1.0", tk.END)
            self.rating_var.set("5")
            self.comment_tc_entry.delete(0, tk.END)
            self.reservation_id_entry.delete(0, tk.END)
            self.controller.show_frame("HotelsPage")
        else:
            messagebox.showerror("Error", result['message'])       

def main():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()