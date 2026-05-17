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

    root = parent.winfo_toplevel()
    if back_page:
        root.set_nav_button("Back", lambda: switch_page(back_page, *back_args))

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

    create_option("Print Ticket",
                  lambda: show_print_ticket_prompt(parent)
                  ).pack(pady=15)

# ===================== FLIGHTS LIST PAGE =====================
def show_flights_list(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent, text="Available Flights", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

    flights = db_utils.get_all_flights()

    # Create a frame for the list (scrollable)
    container = tk.Frame(parent, bg=CARD_COLOR, width=1150, height=380)
    container.pack(padx=20, pady=10, fill="both", expand=True)
    container.pack_propagate(False)

    canvas = tk.Canvas(container, bg=CARD_COLOR, highlightthickness=0, width=1150, height=380)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    list_frame = tk.Frame(canvas, bg=CARD_COLOR)
    canvas.create_window((0, 0), window=list_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    list_frame.bind("<Configure>", on_frame_configure)

    # List header
    header_frame = tk.Frame(list_frame, bg="#475569")
    header_frame.pack(fill="x", padx=10, pady=10)
    tk.Label(header_frame, text="Flight ID", font=("Segoe UI", 10), fg=TEXT_COLOR, bg="#475569", width=18).pack(side="left")
    tk.Label(header_frame, text="Airline", font=("Segoe UI", 10), fg=TEXT_COLOR, bg="#475569", width=18).pack(side="left")
    tk.Label(header_frame, text="From", font=("Segoe UI", 10), fg=TEXT_COLOR, bg="#475569", width=18).pack(side="left")
    tk.Label(header_frame, text="To", font=("Segoe UI", 10), fg=TEXT_COLOR, bg="#475569", width=18).pack(side="left")
    tk.Label(header_frame, text="Departure", font=("Segoe UI", 10), fg=TEXT_COLOR, bg="#475569", width=18).pack(side="left")
    tk.Label(header_frame, text="Status", font=("Segoe UI", 10), fg=TEXT_COLOR, bg="#475569", width=18).pack(side="left")

    # List items
    for flight in flights:
        row_frame = tk.Frame(list_frame, bg=CARD_COLOR)
        row_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(row_frame, text=flight['flight_id'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=18).pack(side="left")
        tk.Label(row_frame, text=flight['airline_id'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=18).pack(side="left")
        tk.Label(row_frame, text=flight['origin'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=18).pack(side="left")
        tk.Label(row_frame, text=flight['destination'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=18).pack(side="left")
        tk.Label(row_frame, text=flight['departure'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=18).pack(side="left")
        
        status_color = "#22c55e" if flight['status'] == "On Schedule" else "#ef4444"
        tk.Label(row_frame, text=flight['status'], font=("Segoe UI", 10), fg=status_color, bg=CARD_COLOR, width=18).pack(side="left")

# ===================== BOOKING FORM PAGE =====================
def show_booking_form(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent, text="Book a Ticket", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

    form_frame = tk.Frame(parent, bg=BG_COLOR)
    form_frame.pack(pady=10, padx=30, fill="none", expand=False)
    form_frame.columnconfigure(1, weight=0)
    
    # Limit form width
    max_width = 500
    form_frame.bind('<Configure>', lambda e: None)

    # Auto-increment Passenger ID
    passengers = db_utils.get_all_passengers()
    if passengers:
        last_id = passengers[-1]['passenger_id']
        prefix = ''.join([c for c in last_id if not c.isdigit()])
        num = int(''.join([c for c in last_id if c.isdigit()])) + 1
        new_pid = f"{prefix}{num:03d}"
    else:
        new_pid = "PASS001"

    tk.Label(form_frame, text="Passenger ID:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).grid(row=0, column=0, sticky="w", pady=8)
    passenger_id_var = tk.StringVar(value=new_pid)
    passenger_id_entry = tk.Entry(form_frame, textvariable=passenger_id_var, width=25, state="disabled")
    passenger_id_entry.grid(row=0, column=1, sticky="ew", pady=8)

    tk.Label(form_frame, text="Passenger Name:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).grid(row=1, column=0, sticky="w", pady=8)
    passenger_name_var = tk.StringVar()
    passenger_name_entry = tk.Entry(form_frame, textvariable=passenger_name_var, width=25)
    passenger_name_entry.grid(row=1, column=1, sticky="ew", pady=8)

    flights = db_utils.get_all_flights()
    sources = sorted({flight['origin'] for flight in flights})

    def get_destinations_for_source(source):
        return sorted({flight['destination'] for flight in flights if flight['origin'] == source})

    def get_available_flights(origin, destination):
        exclude_statuses = {"CHECK-IN OPEN", "BOARDING", "GATE CLOSED", "TAXIING", "DEPARTED", "IN AIR", "ARRIVED"}
        return [flight for flight in flights
                if flight['origin'] == origin
                and flight['destination'] == destination
                and flight.get('status', '').strip().upper() not in exclude_statuses]

    def get_available_seats(flight_id):
        booked = {p['seat'] for p in db_utils.get_passengers_by_flight(flight_id)}
        all_seats = [f"{row}{seat}" for row in range(1, 11) for seat in ["A", "B", "C", "D", "E", "F"]]
        return [seat for seat in all_seats if seat not in booked]

    tk.Label(form_frame, text="Source:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).grid(row=2, column=0, sticky="w", pady=8)
    source_var = tk.StringVar(value=sources[0] if sources else "")
    source_menu = tk.OptionMenu(form_frame, source_var, *sources)
    source_menu.configure(font=("Segoe UI", 11), bg=CARD_COLOR, fg="white", activebackground="#2563eb", relief="flat", width=23)
    source_menu.grid(row=2, column=1, sticky="ew", pady=8)

    tk.Label(form_frame, text="Destination:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).grid(row=3, column=0, sticky="w", pady=8)
    default_destinations = get_destinations_for_source(source_var.get())
    dest_var = tk.StringVar(value=default_destinations[0] if default_destinations else "")
    dest_menu = tk.OptionMenu(form_frame, dest_var, *default_destinations)
    dest_menu.configure(font=("Segoe UI", 11), bg=CARD_COLOR, fg="white", activebackground="#2563eb", relief="flat", width=23)
    dest_menu.grid(row=3, column=1, sticky="ew", pady=8)

    tk.Label(form_frame, text="Select Flight:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).grid(row=4, column=0, sticky="w", pady=8)
    flight_var = tk.StringVar(value="Select a flight")
    flight_menu = tk.OptionMenu(form_frame, flight_var, "Select a flight")
    flight_menu.configure(font=("Segoe UI", 11), bg=CARD_COLOR, fg="white", activebackground="#2563eb", relief="flat", width=37)
    flight_menu.grid(row=4, column=1, sticky="ew", pady=8)

    selected_flight = {'flight': None}
    selected_flight_label = tk.Label(form_frame, text="", font=("Segoe UI", 10), fg=SUB_TEXT, bg=BG_COLOR)
    selected_flight_label.grid(row=5, column=1, sticky="w", pady=(0, 8))

    tk.Label(form_frame, text="Seat Number:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).grid(row=6, column=0, sticky="w", pady=8)
    seat_var = tk.StringVar(value="Select a seat")
    seat_menu = tk.OptionMenu(form_frame, seat_var, "Select a seat")
    seat_menu.configure(font=("Segoe UI", 11), bg=CARD_COLOR, fg="white", activebackground="#2563eb", relief="flat", width=23)
    seat_menu.grid(row=6, column=1, sticky="ew", pady=8)
    seat_menu.config(state="disabled")

    def select_flight(flight):
        selected_flight['flight'] = flight
        flight_var.set(f"{flight['flight_id']} | {flight.get('departure_time') or flight.get('departure')} | {flight.get('status', '')}")
        selected_flight_label.config(text=f"Selected Flight: {flight['flight_id']} | {flight.get('origin')} -> {flight.get('destination')}")
        update_seat_menu()

    def update_destination_menu(*args):
        available_destinations = get_destinations_for_source(source_var.get())
        menu = dest_menu['menu']
        menu.delete(0, 'end')
        for destination in available_destinations:
            menu.add_command(label=destination, command=lambda value=destination: dest_var.set(value))
        if available_destinations:
            dest_var.set(available_destinations[0])
        update_flight_menu()

    def update_flight_menu(*args):
        available_flights = get_available_flights(source_var.get(), dest_var.get())
        menu = flight_menu['menu']
        menu.delete(0, 'end')
        selected_flight['flight'] = None
        selected_flight_label.config(text="")
        seat_menu.config(state="disabled")
        seat_var.set("Select a seat")

        if not available_flights:
            flight_var.set("No flights available")
            menu.add_command(label="No flights available", command=lambda: None)
            return

        flight_var.set("Select a flight")
        for flight in available_flights:
            label = f"{flight['flight_id']} | {flight.get('departure_time') or flight.get('departure')} | {flight.get('status', '')}"
            menu.add_command(label=label, command=lambda f=flight: select_flight(f))

    def update_seat_menu():
        menu = seat_menu['menu']
        menu.delete(0, 'end')
        if not selected_flight['flight']:
            menu.add_command(label="Select a flight first", command=lambda: None)
            seat_var.set("Select a seat")
            seat_menu.config(state="disabled")
            return

        available_seats = get_available_seats(selected_flight['flight']['flight_id'])
        if not available_seats:
            menu.add_command(label="No seats available", command=lambda: None)
            seat_var.set("No seats available")
            seat_menu.config(state="disabled")
            return

        for seat in available_seats:
            menu.add_command(label=seat, command=lambda value=seat: seat_var.set(value))
        seat_var.set(available_seats[0])
        seat_menu.config(state="normal")

    source_var.trace_add('write', update_destination_menu)
    dest_var.trace_add('write', update_flight_menu)
    update_flight_menu()

    def on_book_success():
        if messagebox.askyesno("Print Ticket", "Ticket booked. Do you want to print it now?"):
            show_print_ticket_prompt(parent, passenger_id_var.get())

    def book_ticket():
        if not passenger_name_var.get().strip():
            messagebox.showerror("Error", "Passenger name is required!")
            return
        if not selected_flight['flight']:
            messagebox.showerror("Error", "Please select a valid flight.")
            return
        if seat_var.get() in ["", "Select a seat", "No seats available"]:
            messagebox.showerror("Error", "Please select a valid seat.")
            return

        db_utils.add_passenger(passenger_id_var.get(), passenger_name_var.get(), selected_flight['flight']['flight_id'], seat_var.get())
        messagebox.showinfo("Success", f"Ticket booked successfully for {passenger_name_var.get()}!")
        on_book_success()
        switch_page(back_page, *back_args)

    action_frame = tk.Frame(form_frame, bg=BG_COLOR)
    action_frame.grid(row=7, column=0, columnspan=2, pady=(20, 8))

    tk.Button(action_frame, text="Book Ticket", bg=BTN_SUCCESS, fg="white", relief="flat", font=("Segoe UI", 11, "bold"),
              command=book_ticket).pack(side="left", padx=8)

    tk.Button(action_frame, text="Print Ticket", bg=BTN_PRIMARY, fg="white", relief="flat", font=("Segoe UI", 11, "bold"),
              command=lambda: show_print_ticket_prompt(parent, passenger_id_var.get())).pack(side="left", padx=8)

# ===================== BOOKINGS LIST PAGE =====================
def show_bookings_list(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent, text="Current Bookings", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

    passengers = db_utils.get_all_passengers()

    # Create a frame for the list (scrollable)
    container = tk.Frame(parent, bg=CARD_COLOR, width=1050, height=380)
    container.pack(padx=20, pady=10, fill="both", expand=True)
    container.pack_propagate(False)

    canvas = tk.Canvas(container, bg=CARD_COLOR, highlightthickness=0, width=1050, height=380)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    list_frame = tk.Frame(canvas, bg=CARD_COLOR)
    canvas.create_window((0, 0), window=list_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    list_frame.bind("<Configure>", on_frame_configure)

    # List header
    header_frame = tk.Frame(list_frame, bg="#475569")
    header_frame.pack(fill="x", padx=10, pady=10)
    tk.Label(header_frame, text="Passenger ID", font=("Segoe UI", 10), fg=TEXT_COLOR, bg="#475569", width=20).pack(side="left")
    tk.Label(header_frame, text="Name", font=("Segoe UI", 10), fg=TEXT_COLOR, bg="#475569", width=22).pack(side="left")
    tk.Label(header_frame, text="Flight ID", font=("Segoe UI", 10), fg=TEXT_COLOR, bg="#475569", width=18).pack(side="left")
    tk.Label(header_frame, text="Seat", font=("Segoe UI", 10), fg=TEXT_COLOR, bg="#475569", width=15).pack(side="left")

    # List items
    for passenger in passengers:
        row_frame = tk.Frame(list_frame, bg=CARD_COLOR)
        row_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(row_frame, text=passenger['passenger_id'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=20).pack(side="left")
        tk.Label(row_frame, text=passenger['name'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=22).pack(side="left")
        tk.Label(row_frame, text=passenger['flight_id'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=18).pack(side="left")
        tk.Label(row_frame, text=passenger['seat'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=15).pack(side="left")


def show_print_ticket_prompt(parent, default_passenger_id=None):
    root_window = parent.winfo_toplevel() if hasattr(parent, 'winfo_toplevel') else parent
    prompt_win = tk.Toplevel(root_window)
    prompt_win.title("Print Ticket")
    prompt_win.configure(bg=BG_COLOR)
    prompt_win.geometry("420x380")

    tk.Label(prompt_win, text="Print Ticket", font=("Segoe UI", 18, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=15)

    tk.Label(prompt_win, text="Enter Passenger ID:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=(10, 5))
    passenger_id_var = tk.StringVar(value=default_passenger_id or "")
    passenger_id_entry = tk.Entry(prompt_win, textvariable=passenger_id_var, width=30)
    passenger_id_entry.pack(pady=5)

    ticket_frame = tk.Frame(prompt_win, bg=BG_COLOR)
    ticket_frame.pack(fill="both", expand=True, padx=15, pady=10)

    def render_ticket(passenger):
        for w in ticket_frame.winfo_children():
            w.destroy()

        flight = next((f for f in db_utils.get_all_flights() if f['flight_id'] == passenger['flight_id']), None)
        ticket_text = (
            f"Passenger ID: {passenger['passenger_id']}\n"
            f"Name: {passenger['name']}\n"
            f"Flight ID: {passenger['flight_id']}\n"
            f"Seat: {passenger['seat']}\n"
            f"Checked In: {passenger.get('checked_in', 'No')}\n"
            f"Baggage Weight: {passenger.get('baggage_weight', '0')} kg\n"
            + (f"Airline: {flight['airline_id']}\nOrigin: {flight['origin']}\nDestination: {flight['destination']}\nDeparture: {flight['departure']}\nArrival: {flight['arrival']}\nStatus: {flight['status']}\n" if flight else "")
        )

        ticket_card = tk.Label(ticket_frame,
                               text=ticket_text,
                               justify="left",
                               bg="white",
                               fg="black",
                               font=("Consolas", 10),
                               bd=2,
                               relief="solid",
                               padx=10,
                               pady=10)
        ticket_card.pack(fill="both", expand=True)

    def show_ticket():
        pid = passenger_id_var.get().strip()
        if not pid:
            messagebox.showerror("Error", "Passenger ID is required.")
            return
        passenger = next((p for p in db_utils.get_all_passengers() if p['passenger_id'] == pid), None)
        if not passenger:
            messagebox.showerror("Not Found", f"No passenger found with ID {pid}.")
            return
        render_ticket(passenger)

    tk.Button(prompt_win, text="Show Ticket", bg=BTN_SUCCESS, fg="white", relief="flat", font=("Segoe UI", 11, "bold"), command=show_ticket).pack(pady=10)

    # Automatically display the ticket when a default passenger ID is provided (e.g. after booking)
    if default_passenger_id:
        show_ticket()
