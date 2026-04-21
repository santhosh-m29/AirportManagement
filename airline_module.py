# airline_module.py

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
def show_airline_dashboard(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent,
             text="MANAGE AIRLINES",
             font=("Segoe UI", 24, "bold"),
             fg=TEXT_COLOR,
             bg=BG_COLOR).pack(pady=40)

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
    
    create_option("Edit Airlines",
                  lambda: switch_page(show_edit_airlines, show_airline_dashboard, (back_page, back_args))
                  ).pack(pady=15)

    # Removed 'Add Flights' from dashboard options

    create_option("Edit Flights",
                  lambda: switch_page(show_edit_flights, show_airline_dashboard, (back_page, back_args))
                  ).pack(pady=15)

    create_option("Airline Information",
                  lambda: switch_page(show_airline_information, show_airline_dashboard, (back_page, back_args))
                  ).pack(pady=15)

    create_option("Pilot / Crew Data",
                  lambda: switch_page(show_crew_data, show_airline_dashboard, (back_page, back_args))
                  ).pack(pady=15)

# ===================== EDIT AIRLINES PAGE =====================
def show_edit_airlines(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent,
             text="Edit Airlines",
             font=("Segoe UI", 22, "bold"),
             fg=TEXT_COLOR,
             bg=BG_COLOR).pack(pady=20)

    # Get all airlines
    airlines = db_utils.get_all_airlines()

    # Create a frame for the list
    list_frame = tk.Frame(parent, bg=CARD_COLOR, width=800, height=400)
    list_frame.pack(padx=20, pady=10, fill="both", expand=True)
    list_frame.pack_propagate(False)

    # List header
    header_frame = tk.Frame(list_frame, bg="#475569")
    header_frame.pack(fill="x", padx=10, pady=10)
    tk.Label(header_frame, text="ID", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=10).pack(side="left")
    tk.Label(header_frame, text="Name", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=20).pack(side="left")
    tk.Label(header_frame, text="Flights", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=10).pack(side="left")
    tk.Label(header_frame, text="Actions", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=20).pack(side="left")

    # List items
    for airline in airlines:
        row_frame = tk.Frame(list_frame, bg=CARD_COLOR)
        row_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(row_frame, text=airline['airline_id'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=10).pack(side="left")
        tk.Label(row_frame, text=airline['name'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=20).pack(side="left")
        tk.Label(row_frame, text=airline['flights'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=10).pack(side="left")
        
        action_frame = tk.Frame(row_frame, bg=CARD_COLOR)
        action_frame.pack(side="left", fill="x", expand=True)
        tk.Button(action_frame, text="Edit", bg=BTN_PRIMARY, fg="white", relief="flat", width=8,
                  command=lambda aid=airline['airline_id']: switch_page(show_edit_airline_form, show_edit_airlines, (back_page, back_args))).pack(side="left", padx=5)
        tk.Button(action_frame, text="Delete", bg=BTN_DANGER, fg="white", relief="flat", width=8,
                  command=lambda aid=airline['airline_id']: delete_airline_action(aid, switch_page, show_edit_airlines, (back_page, back_args))).pack(side="left", padx=5)

    # Add new airline button
    button_frame = tk.Frame(parent, bg=BG_COLOR)
    button_frame.pack(pady=20)
    tk.Button(button_frame, text="+ Add New Airline", font=("Segoe UI", 12, "bold"), bg=BTN_SUCCESS, 
              fg="white", relief="flat", command=lambda: switch_page(show_add_airline_form, show_edit_airlines, (back_page, back_args))).pack()

def delete_airline_action(airline_id, switch_page, current_page, back_args_tuple):
    if messagebox.askyesno("Confirm", "Are you sure you want to delete this airline?"):
        db_utils.delete_airline(airline_id)
        messagebox.showinfo("Success", "Airline deleted successfully!")
        switch_page(current_page, *back_args_tuple)

def show_edit_airline_form(parent, switch_page, back_page, back_args, airline_id):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    airlines = db_utils.get_all_airlines()
    airline = next((a for a in airlines if a['airline_id'] == airline_id), None)

    if not airline:
        messagebox.showerror("Error", "Airline not found!")
        switch_page(show_edit_airlines, back_page, back_args)
        return

    tk.Label(parent, text="Edit Airline", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

    form_frame = tk.Frame(parent, bg=BG_COLOR)
    form_frame.pack(pady=20)

    tk.Label(form_frame, text="Airline ID:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w")
    id_var = tk.StringVar(value=airline['airline_id'])
    id_entry = tk.Entry(form_frame, textvariable=id_var, width=30, state="disabled")
    id_entry.pack(pady=5)

    tk.Label(form_frame, text="Airline Name:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    name_var = tk.StringVar(value=airline['name'])
    name_entry = tk.Entry(form_frame, textvariable=name_var, width=30)
    name_entry.pack(pady=5)
    name_entry.bind("<Return>", lambda e: save_changes())

    tk.Label(form_frame, text="Number of Flights:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    flights_var = tk.StringVar(value=airline['flights'])
    flights_entry = tk.Entry(form_frame, textvariable=flights_var, width=30)
    flights_entry.pack(pady=5)
    flights_entry.bind("<Return>", lambda e: save_changes())

    def save_changes():
        db_utils.update_airline(airline_id, name_var.get(), flights_var.get())
        messagebox.showinfo("Success", "Airline updated successfully!")
        switch_page(back_page, *back_args)

    tk.Button(form_frame, text="Save Changes", bg=BTN_SUCCESS, fg="white", relief="flat", font=("Segoe UI", 11, "bold"),
              command=save_changes).pack(pady=20)

def show_add_airline_form(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent, text="Add New Airline", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

    form_frame = tk.Frame(parent, bg=BG_COLOR)
    form_frame.pack(pady=20)


    # Auto-increment Airline ID
    airlines = db_utils.get_all_airlines()
    if airlines:
        last_id = airlines[-1]['airline_id']
        prefix = ''.join([c for c in last_id if not c.isdigit()])
        num = int(''.join([c for c in last_id if c.isdigit()])) + 1
        new_id = f"{prefix}{num:03d}"
    else:
        new_id = "AIR001"
    tk.Label(form_frame, text="Airline ID:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w")
    id_var = tk.StringVar(value=new_id)
    id_entry = tk.Entry(form_frame, textvariable=id_var, width=30, state="disabled")
    id_entry.pack(pady=5)

    tk.Label(form_frame, text="Airline Name:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    name_var = tk.StringVar()
    name_entry = tk.Entry(form_frame, textvariable=name_var, width=30)
    name_entry.pack(pady=5)
    name_entry.bind("<Return>", lambda e: add_airline())

    tk.Label(form_frame, text="Number of Flights:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    flights_var = tk.StringVar(value="0")
    flights_entry = tk.Entry(form_frame, textvariable=flights_var, width=30)
    flights_entry.pack(pady=5)
    flights_entry.bind("<Return>", lambda e: add_airline())


    def add_airline():
        if not name_var.get():
            messagebox.showerror("Error", "All fields are required!")
            return
        db_utils.add_airline(id_var.get(), name_var.get(), flights_var.get())
        messagebox.showinfo("Success", "Airline added successfully!")
        switch_page(back_page, *back_args)

    tk.Button(form_frame, text="Add Airline", bg=BTN_SUCCESS, fg="white", relief="flat", font=("Segoe UI", 11, "bold"),
              command=add_airline).pack(pady=20)

# ===================== ADD FLIGHTS FORM =====================
def show_add_flights_form(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent, text="Add New Flight", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

    form_frame = tk.Frame(parent, bg=BG_COLOR)
    form_frame.pack(pady=20)

    # Auto-increment Flight ID
    flights = db_utils.get_all_flights()
    if flights:
        last_id = flights[-1]['flight_id']
        prefix = ''.join([c for c in last_id if not c.isdigit()])
        num = int(''.join([c for c in last_id if c.isdigit()])) + 1
        new_id = f"{prefix}{num:03d}"
    else:
        new_id = "FL001"
    tk.Label(form_frame, text="Flight ID:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w")
    id_var = tk.StringVar(value=new_id)
    id_entry = tk.Entry(form_frame, textvariable=id_var, width=30, state="disabled")
    id_entry.pack(pady=5)

    # Airline selection
    tk.Label(form_frame, text="Select Airline:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    airlines = db_utils.get_all_airlines()
    airline_options = [f"{a['airline_id']} - {a['name']}" for a in airlines]
    airline_var = tk.StringVar()
    if airline_options:
        airline_var.set(airline_options[0])
    airline_menu = tk.OptionMenu(form_frame, airline_var, *airline_options)
    airline_menu.config(bg=CARD_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 10), width=27)
    airline_menu.pack(pady=5)

    tk.Label(form_frame, text="Source (Origin):", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    origin_var = tk.StringVar()
    origin_entry = tk.Entry(form_frame, textvariable=origin_var, width=30)
    origin_entry.pack(pady=5)

    tk.Label(form_frame, text="Destination:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    destination_var = tk.StringVar()
    destination_entry = tk.Entry(form_frame, textvariable=destination_var, width=30)
    destination_entry.pack(pady=5)

    tk.Label(form_frame, text="Start Time (Departure):", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    departure_var = tk.StringVar()
    departure_entry = tk.Entry(form_frame, textvariable=departure_var, width=30)
    departure_entry.pack(pady=5)

    tk.Label(form_frame, text="End Time (Arrival):", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    arrival_var = tk.StringVar()
    arrival_entry = tk.Entry(form_frame, textvariable=arrival_var, width=30)
    arrival_entry.pack(pady=5)

    def add_flight():
        if not all([airline_var.get(), origin_var.get(), destination_var.get(), departure_var.get(), arrival_var.get()]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        # Extract airline_id from selection
        airline_id = airline_var.get().split(' - ')[0]
        
        # Auto-assign gate and runway
        gates = db_utils.get_all_gates()
        runways = db_utils.get_all_runways()
        
        available_gate = next((g for g in gates if g['status'] == 'Available'), None)
        available_runway = next((r for r in runways if r['status'] == 'Available'), None)
        
        if not available_gate:
            messagebox.showerror("Error", "No available gates!")
            return
        if not available_runway:
            messagebox.showerror("Error", "No available runways!")
            return
        
        gate = available_gate['gate_id']
        runway = available_runway['runway_id']
        
        db_utils.add_flight(id_var.get(), airline_id, origin_var.get(), destination_var.get(), departure_var.get(), arrival_var.get(), gate, runway)
        
        # Update gate and runway status to In Use
        db_utils.update_gate_status(gate, "In Use")
        db_utils.update_runway_status(runway, "In Use")
        
        # Update airline flight count
        current_airlines = db_utils.get_all_airlines()
        airline = next((a for a in current_airlines if a['airline_id'] == airline_id), None)
        if airline:
            current_flights = int(airline['flights'])
            db_utils.update_airline(airline_id, airline['name'], str(current_flights + 1))
        
        messagebox.showinfo("Success", "Flight added successfully!")
        switch_page(back_page, *back_args)

    tk.Button(form_frame, text="Add Flight", bg=BTN_SUCCESS, fg="white", relief="flat", font=("Segoe UI", 11, "bold"),
              command=add_flight).pack(pady=20)

# ===================== EDIT FLIGHTS PAGE =====================
def show_edit_flights(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent,
             text="Edit Flights",
             font=("Segoe UI", 22, "bold"),
             fg=TEXT_COLOR,
             bg=BG_COLOR).pack(pady=20)

    # Get all flights
    flights = db_utils.get_all_flights()

    # Create a frame for the list
    list_frame = tk.Frame(parent, bg=CARD_COLOR, width=1000, height=400)
    list_frame.pack(padx=20, pady=10, fill="both", expand=True)
    list_frame.pack_propagate(False)

    # List header
    header_frame = tk.Frame(list_frame, bg="#475569")
    header_frame.pack(fill="x", padx=10, pady=10)
    tk.Label(header_frame, text="Flight ID", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=10).pack(side="left")
    tk.Label(header_frame, text="Airline", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=15).pack(side="left")
    tk.Label(header_frame, text="Origin", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=15).pack(side="left")
    tk.Label(header_frame, text="Destination", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=15).pack(side="left")
    tk.Label(header_frame, text="Departure", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=10).pack(side="left")
    tk.Label(header_frame, text="Arrival", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=10).pack(side="left")
    tk.Label(header_frame, text="Status", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=12).pack(side="left")
    tk.Label(header_frame, text="Actions", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=15).pack(side="left")

    # List items
    for flight in flights:
        row_frame = tk.Frame(list_frame, bg=CARD_COLOR)
        row_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(row_frame, text=flight['flight_id'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=10).pack(side="left")
        tk.Label(row_frame, text=flight['airline_id'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=15).pack(side="left")
        tk.Label(row_frame, text=flight['origin'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=15).pack(side="left")
        tk.Label(row_frame, text=flight['destination'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=15).pack(side="left")
        tk.Label(row_frame, text=flight['departure'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=10).pack(side="left")
        tk.Label(row_frame, text=flight['arrival'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=10).pack(side="left")
        tk.Label(row_frame, text=flight['status'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=12).pack(side="left")
        
        action_frame = tk.Frame(row_frame, bg=CARD_COLOR)
        action_frame.pack(side="left", fill="x", expand=True)
        tk.Button(action_frame, text="Edit", bg=BTN_PRIMARY, fg="white", relief="flat", width=6,
                  command=lambda fid=flight['flight_id']: switch_page(show_edit_flight_form, show_edit_flights, (back_page, back_args), fid)).pack(side="left", padx=5)
        tk.Button(action_frame, text="Delete", bg=BTN_DANGER, fg="white", relief="flat", width=6,
                  command=lambda fid=flight['flight_id']: delete_flight_action(fid, switch_page, show_edit_flights, (back_page, back_args))).pack(side="left", padx=5)

    # Add Flights button at the bottom
    tk.Button(parent, text="Add Flight", bg=BTN_SUCCESS, fg="white", relief="flat", font=("Segoe UI", 11, "bold"),
              command=lambda: switch_page(show_add_flights_form, show_edit_flights, (back_page, back_args))).pack(pady=20)

def delete_flight_action(flight_id, switch_page, current_page, back_args_tuple):
    if messagebox.askyesno("Confirm", "Are you sure you want to delete this flight?"):
        # Get flight details to free up gate and runway
        flights = db_utils.get_all_flights()
        flight = next((f for f in flights if f['flight_id'] == flight_id), None)
        if flight:
            db_utils.update_gate_status(flight['gate'], "Available")
            db_utils.update_runway_status(flight['runway'], "Available")
            # Update airline flight count
            airlines = db_utils.get_all_airlines()
            airline = next((a for a in airlines if a['airline_id'] == flight['airline_id']), None)
            if airline:
                current_flights = int(airline['flights'])
                db_utils.update_airline(flight['airline_id'], airline['name'], str(current_flights - 1))
        
        # Remove flight
        db_utils.delete_flight(flight_id)
        messagebox.showinfo("Success", "Flight deleted successfully!")
        switch_page(current_page, *back_args_tuple)

def show_edit_flight_form(parent, switch_page, back_page, back_args, flight_id):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    flights = db_utils.get_all_flights()
    flight = next((f for f in flights if f['flight_id'] == flight_id), None)

    if not flight:
        messagebox.showerror("Error", "Flight not found!")
        switch_page(show_edit_flights, back_page, back_args)
        return

    tk.Label(parent, text="Edit Flight", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

    form_frame = tk.Frame(parent, bg=BG_COLOR)
    form_frame.pack(pady=20)

    tk.Label(form_frame, text="Flight ID:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w")
    id_var = tk.StringVar(value=flight['flight_id'])
    id_entry = tk.Entry(form_frame, textvariable=id_var, width=30)
    id_entry.pack(pady=5)

    # Airline selection
    tk.Label(form_frame, text="Select Airline:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    airlines = db_utils.get_all_airlines()
    airline_options = [f"{a['airline_id']} - {a['name']}" for a in airlines]
    current_airline_option = next((opt for opt in airline_options if opt.startswith(flight['airline_id'])), airline_options[0] if airline_options else "")
    airline_var = tk.StringVar(value=current_airline_option)
    airline_menu = tk.OptionMenu(form_frame, airline_var, *airline_options)
    airline_menu.config(bg=CARD_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 10), width=27)
    airline_menu.pack(pady=5)

    tk.Label(form_frame, text="Source (Origin):", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    origin_var = tk.StringVar(value=flight['origin'])
    origin_entry = tk.Entry(form_frame, textvariable=origin_var, width=30)
    origin_entry.pack(pady=5)

    tk.Label(form_frame, text="Destination:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    destination_var = tk.StringVar(value=flight['destination'])
    destination_entry = tk.Entry(form_frame, textvariable=destination_var, width=30)
    destination_entry.pack(pady=5)

    tk.Label(form_frame, text="Start Time (Departure):", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    departure_var = tk.StringVar(value=flight['departure'])
    departure_entry = tk.Entry(form_frame, textvariable=departure_var, width=30)
    departure_entry.pack(pady=5)

    tk.Label(form_frame, text="End Time (Arrival):", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    arrival_var = tk.StringVar(value=flight['arrival'])
    arrival_entry = tk.Entry(form_frame, textvariable=arrival_var, width=30)
    arrival_entry.pack(pady=5)

    tk.Label(form_frame, text="Gate:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    gates = db_utils.get_all_gates()
    gate_options = [g['gate_id'] for g in gates]
    gate_var = tk.StringVar(value=flight['gate'])
    gate_menu = tk.OptionMenu(form_frame, gate_var, *gate_options)
    gate_menu.config(bg=CARD_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 10), width=27)
    gate_menu.pack(pady=5)

    tk.Label(form_frame, text="Runway:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    runways = db_utils.get_all_runways()
    runway_options = [r['runway_id'] for r in runways]
    runway_var = tk.StringVar(value=flight['runway'])
    runway_menu = tk.OptionMenu(form_frame, runway_var, *runway_options)
    runway_menu.config(bg=CARD_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 10), width=27)
    runway_menu.pack(pady=5)

    tk.Label(form_frame, text="Status:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    status_options = ["On Schedule", "Delayed", "Cancelled", "Boarding", "Departed", "Arrived"]
    status_var = tk.StringVar(value=flight['status'])
    status_menu = tk.OptionMenu(form_frame, status_var, *status_options)
    status_menu.config(bg=CARD_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 10), width=27)
    status_menu.pack(pady=5)

    def save_changes():
        if not all([id_var.get(), airline_var.get(), origin_var.get(), destination_var.get(), departure_var.get(), arrival_var.get(), gate_var.get(), runway_var.get(), status_var.get()]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        # Extract airline_id
        airline_id = airline_var.get().split(' - ')[0]
        
        # If gate or runway changed, update statuses
        if gate_var.get() != flight['gate']:
            db_utils.update_gate_status(flight['gate'], "Available")
            db_utils.update_gate_status(gate_var.get(), "In Use")
        if runway_var.get() != flight['runway']:
            db_utils.update_runway_status(flight['runway'], "Available")
            db_utils.update_runway_status(runway_var.get(), "In Use")
        
        # If airline changed, update flight counts
        if airline_id != flight['airline_id']:
            # Decrease old airline count
            airlines = db_utils.get_all_airlines()
            old_airline = next((a for a in airlines if a['airline_id'] == flight['airline_id']), None)
            if old_airline:
                current_flights = int(old_airline['flights'])
                db_utils.update_airline(flight['airline_id'], old_airline['name'], str(current_flights - 1))
            # Increase new airline count
            new_airline = next((a for a in airlines if a['airline_id'] == airline_id), None)
            if new_airline:
                current_flights = int(new_airline['flights'])
                db_utils.update_airline(airline_id, new_airline['name'], str(current_flights + 1))
        
        db_utils.update_flight(flight_id, id_var.get(), airline_id, origin_var.get(), destination_var.get(), departure_var.get(), arrival_var.get(), gate_var.get(), runway_var.get(), status_var.get())
        messagebox.showinfo("Success", "Flight updated successfully!")
        switch_page(back_page, *back_args)

    tk.Button(form_frame, text="Save Changes", bg=BTN_SUCCESS, fg="white", relief="flat", font=("Segoe UI", 11, "bold"),
              command=save_changes).pack(pady=20)

# ===================== AIRLINE INFORMATION PAGE =====================
def show_airline_information(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent, text="Airline Information", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

    airlines = db_utils.get_all_airlines()

    info_frame = tk.Frame(parent, bg=BG_COLOR)
    info_frame.pack(padx=20, pady=20, fill="both", expand=True)

    for airline in airlines:
        card = tk.Frame(info_frame, bg=CARD_COLOR, height=80)
        card.pack(fill="x", padx=10, pady=10)
        card.pack_propagate(False)

        tk.Label(card, text=f"{airline['name']}", font=("Segoe UI", 13, "bold"), fg=TEXT_COLOR, bg=CARD_COLOR).pack(anchor="w", padx=15, pady=10)
        tk.Label(card, text=f"ID: {airline['airline_id']} | Fleet Size: {airline['flights']} aircraft", 
                 font=("Segoe UI", 10), fg=SUB_TEXT, bg=CARD_COLOR).pack(anchor="w", padx=15, pady=5)

# ===================== CREW DATA PAGE =====================
def show_crew_data(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent, text="Pilot / Crew Data", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

    # Get all crew
    crew = db_utils.get_all_crew()

    # Create a frame for the list
    list_frame = tk.Frame(parent, bg=CARD_COLOR, width=900, height=400)
    list_frame.pack(padx=20, pady=10, fill="both", expand=True)
    list_frame.pack_propagate(False)

    # List header
    header_frame = tk.Frame(list_frame, bg="#475569")
    header_frame.pack(fill="x", padx=10, pady=10)
    tk.Label(header_frame, text="Crew ID", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=12).pack(side="left")
    tk.Label(header_frame, text="Name", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=20).pack(side="left")
    tk.Label(header_frame, text="Role", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=15).pack(side="left")
    tk.Label(header_frame, text="Airline", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=15).pack(side="left")

    # List items
    for member in crew:
        row_frame = tk.Frame(list_frame, bg=CARD_COLOR)
        row_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(row_frame, text=member['crew_id'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=12).pack(side="left")
        tk.Label(row_frame, text=member['name'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=20).pack(side="left")
        tk.Label(row_frame, text=member['role'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=15).pack(side="left")
        tk.Label(row_frame, text=member['airline_id'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=15).pack(side="left")

