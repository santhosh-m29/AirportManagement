# ticket_module.py

import tkinter as tk
from tkinter import messagebox
import db_utils

# ===================== THEME COLORS =====================
BG_COLOR = "#0f172a"
CARD_COLOR = "#1e293b"
TEXT_COLOR = "white"
SUB_TEXT = "#cbd5e1"
BTN_PRIMARY = "#2563eb"
BTN_SUCCESS = "#22c55e"
BTN_DANGER = "#ef4444"
BTN_SECONDARY = "#475569"

# ===================== HEADER =====================
def create_header(parent, switch_page, back_page, back_args):
    header = tk.Frame(parent, bg=BG_COLOR)
    header.pack(fill="x", pady=10)

    tk.Button(header,
              text="Back",
              bg=BTN_DANGER,
              fg="white",
              font=("Segoe UI", 10, "bold"),
              relief="flat",
              command=lambda: switch_page(back_page, *back_args)
              ).pack(side="left", padx=20)

# ===================== MAIN DASHBOARD =====================
def show_ticket_dashboard(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent,
             text="TICKET COUNTER",
             font=("Segoe UI", 24, "bold"),
             fg=TEXT_COLOR,
             bg=BG_COLOR).pack(pady=30)

    button_frame = tk.Frame(parent, bg=BG_COLOR)
    button_frame.pack()

    def create_option(text, command):
        return tk.Button(button_frame,
                         text=text,
                         font=("Segoe UI", 13, "bold"),
                         width=25,
                         height=2,
                         bg=BTN_PRIMARY,
                         fg="white",
                         relief="flat",
                         command=command)
    
    create_option("View Available Flights",
                  lambda: switch_page(show_flights_list, show_ticket_dashboard, (back_page, back_args))
                  ).pack(pady=15)

    create_option("Book Ticket",
                  lambda: switch_page(show_booking_form, show_ticket_dashboard, (back_page, back_args))
                  ).pack(pady=15)

    create_option("View Bookings",
                  lambda: switch_page(show_bookings_list, show_ticket_dashboard, (back_page, back_args))
                  ).pack(pady=15)

# ===================== FLIGHTS LIST PAGE =====================
def show_flights_list(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent, text="Available Flights", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

    flights = db_utils.get_all_flights()

    # Create a frame for the list
    list_frame = tk.Frame(parent, bg=CARD_COLOR, width=950, height=380)
    list_frame.pack(padx=20, pady=10, fill="both", expand=True)
    list_frame.pack_propagate(False)

    # List header
    header_frame = tk.Frame(list_frame, bg="#475569")
    header_frame.pack(fill="x", padx=10, pady=10)
    tk.Label(header_frame, text="Flight ID", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=12).pack(side="left")
    tk.Label(header_frame, text="Airline", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=12).pack(side="left")
    tk.Label(header_frame, text="From", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=12).pack(side="left")
    tk.Label(header_frame, text="To", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=12).pack(side="left")
    tk.Label(header_frame, text="Departure", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=12).pack(side="left")
    tk.Label(header_frame, text="Status", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=12).pack(side="left")

    # List items
    for flight in flights:
        row_frame = tk.Frame(list_frame, bg=CARD_COLOR)
        row_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(row_frame, text=flight['flight_id'], font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=12).pack(side="left")
        tk.Label(row_frame, text=flight['airline_id'], font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=12).pack(side="left")
        tk.Label(row_frame, text=flight['origin'], font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=12).pack(side="left")
        tk.Label(row_frame, text=flight['destination'], font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=12).pack(side="left")
        tk.Label(row_frame, text=flight['departure'], font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=12).pack(side="left")
        
        status_color = "#22c55e" if flight['status'] == "On Schedule" else "#ef4444"
        tk.Label(row_frame, text=flight['status'], font=("Segoe UI", 9), fg=status_color, bg=CARD_COLOR, width=12).pack(side="left")

# ===================== BOOKING FORM PAGE =====================
def show_booking_form(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent, text="Book a Ticket", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

    form_frame = tk.Frame(parent, bg=BG_COLOR)
    form_frame.pack(pady=20)

    # Auto-increment Passenger ID
    passengers = db_utils.get_all_passengers()
    if passengers:
        last_id = passengers[-1]['passenger_id']
        prefix = ''.join([c for c in last_id if not c.isdigit()])
        num = int(''.join([c for c in last_id if c.isdigit()])) + 1
        new_pid = f"{prefix}{num:03d}"
    else:
        new_pid = "PASS001"
    tk.Label(form_frame, text="Passenger ID:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w")
    passenger_id_var = tk.StringVar(value=new_pid)
    passenger_id_entry = tk.Entry(form_frame, textvariable=passenger_id_var, width=30, state="disabled")
    passenger_id_entry.pack(pady=5)

    tk.Label(form_frame, text="Passenger Name:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    passenger_name_var = tk.StringVar()
    passenger_name_entry = tk.Entry(form_frame, textvariable=passenger_name_var, width=30)
    passenger_name_entry.pack(pady=5)

    # Source and Destination
    tk.Label(form_frame, text="Source:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    source_var = tk.StringVar()
    source_entry = tk.Entry(form_frame, textvariable=source_var, width=30)
    source_entry.pack(pady=5)

    tk.Label(form_frame, text="Destination:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    dest_var = tk.StringVar()
    dest_entry = tk.Entry(form_frame, textvariable=dest_var, width=30)
    dest_entry.pack(pady=5)

    # Button to search flights
    def show_flights():
        flights = [f for f in db_utils.get_all_flights() if f['origin'].lower() == source_var.get().strip().lower() and f['destination'].lower() == dest_var.get().strip().lower()]
        if not flights:
            messagebox.showinfo("No Flights", "No flights found for the selected route.")
            return
        # Show flights in a new window for selection
        select_win = tk.Toplevel(parent)
        select_win.title("Select Flight")
        select_win.configure(bg=BG_COLOR)
        tk.Label(select_win, text="Select a Flight", font=("Segoe UI", 14, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=10)
        for flight in flights:
            btn = tk.Button(select_win, text=f"{flight['flight_id']} | {flight['origin']} -> {flight['destination']} | {flight['departure']}",
                            font=("Segoe UI", 11), bg=BTN_PRIMARY, fg="white", relief="flat",
                            command=lambda f=flight: select_flight(f, select_win))
            btn.pack(pady=5, padx=10, fill="x")

    selected_flight = {'flight_id': None}

    def select_flight(flight, win):
        selected_flight['flight_id'] = flight['flight_id']
        win.destroy()
        seat_entry.focus_set()

    tk.Button(form_frame, text="Show Available Flights", bg=BTN_SECONDARY, fg="white", relief="flat", font=("Segoe UI", 11, "bold"),
              command=show_flights).pack(pady=10)

    tk.Label(form_frame, text="Seat Number:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    seat_var = tk.StringVar()
    seat_entry = tk.Entry(form_frame, textvariable=seat_var, width=30)
    seat_entry.pack(pady=5)

    def book_ticket():
        if not all([passenger_name_var.get(), source_var.get(), dest_var.get(), seat_var.get()]):
            messagebox.showerror("Error", "All fields are required!")
            return
        if not selected_flight['flight_id']:
            messagebox.showerror("Error", "Please select a flight.")
            return
        db_utils.add_passenger(passenger_id_var.get(), passenger_name_var.get(), selected_flight['flight_id'], seat_var.get())
        messagebox.showinfo("Success", f"Ticket booked successfully for {passenger_name_var.get()}!")
        switch_page(back_page, *back_args)

    tk.Button(form_frame, text="Book Ticket", bg=BTN_SUCCESS, fg="white", relief="flat", font=("Segoe UI", 11, "bold"),
              command=book_ticket).pack(pady=20)

# ===================== BOOKINGS LIST PAGE =====================
def show_bookings_list(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent, text="Current Bookings", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

    passengers = db_utils.get_all_passengers()

    # Create a frame for the list
    list_frame = tk.Frame(parent, bg=CARD_COLOR, width=900, height=380)
    list_frame.pack(padx=20, pady=10, fill="both", expand=True)
    list_frame.pack_propagate(False)

    # List header
    header_frame = tk.Frame(list_frame, bg="#475569")
    header_frame.pack(fill="x", padx=10, pady=10)
    tk.Label(header_frame, text="Passenger ID", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=15).pack(side="left")
    tk.Label(header_frame, text="Name", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=15).pack(side="left")
    tk.Label(header_frame, text="Flight ID", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=12).pack(side="left")
    tk.Label(header_frame, text="Seat", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=10).pack(side="left")

    # List items
    for passenger in passengers:
        row_frame = tk.Frame(list_frame, bg=CARD_COLOR)
        row_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(row_frame, text=passenger['passenger_id'], font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=15).pack(side="left")
        tk.Label(row_frame, text=passenger['name'], font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=15).pack(side="left")
        tk.Label(row_frame, text=passenger['flight_id'], font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=12).pack(side="left")
        tk.Label(row_frame, text=passenger['seat'], font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=10).pack(side="left")