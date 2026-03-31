# atc_module.py

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
def show_atc_dashboard(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent,
             text="ATC OPERATIONS",
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
    
    create_option("Gate Management",
                  lambda: switch_page(show_gate_management, show_atc_dashboard, (back_page, back_args))
                  ).pack(pady=15)

    create_option("Runway Management",
                  lambda: switch_page(show_runway_management, show_atc_dashboard, (back_page, back_args))
                  ).pack(pady=15)

    create_option("Flight Schedule",
                  lambda: switch_page(show_flight_schedule, show_atc_dashboard, (back_page, back_args))
                  ).pack(pady=15)

    create_option("Flight Status Updates",
                  lambda: switch_page(show_flight_status, show_atc_dashboard, (back_page, back_args))
                  ).pack(pady=15)

# ===================== GATE MANAGEMENT PAGE =====================
def show_gate_management(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent, text="Gate Management", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

    gates = db_utils.get_all_gates()

    # Add a canvas and scrollbar for scrolling
    container = tk.Frame(parent, bg=CARD_COLOR, width=700, height=350)
    container.pack(padx=20, pady=10, fill="both", expand=True)
    container.pack_propagate(False)

    canvas = tk.Canvas(container, bg=CARD_COLOR, highlightthickness=0, width=700, height=350)
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
    tk.Label(header_frame, text="Gate ID", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=12).pack(side="left")
    tk.Label(header_frame, text="Terminal", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=15).pack(side="left")
    tk.Label(header_frame, text="Status", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=15).pack(side="left")
    tk.Label(header_frame, text="Actions", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=15).pack(side="left")

    # List items
    for gate in gates:
        row_frame = tk.Frame(list_frame, bg=CARD_COLOR)
        row_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(row_frame, text=gate['gate_id'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=12).pack(side="left")
        tk.Label(row_frame, text=gate['terminal'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=15).pack(side="left")
        status_color = "#22c55e" if gate['status'] == "Available" else "#ef4444"
        tk.Label(row_frame, text=gate['status'], font=("Segoe UI", 10), fg=status_color, bg=CARD_COLOR, width=15).pack(side="left")
        if gate['status'] == "Available":
            action_text = "Occupy"
            new_status = "Occupied"
        else:
            action_text = "Release"
            new_status = "Available"
        tk.Button(row_frame, text=action_text, bg=BTN_PRIMARY, fg="white", relief="flat", width=8,
                  command=lambda gid=gate['gate_id'], ns=new_status: update_gate_status(gid, ns, switch_page, show_gate_management, back_page, back_args)).pack(side="left", padx=5)

def update_gate_status(gate_id, new_status, switch_page, current_page, back_page, back_args):
    db_utils.update_gate_status(gate_id, new_status)
    messagebox.showinfo("Success", f"Gate {gate_id} status updated to {new_status}!")
    switch_page(current_page, back_page, back_args)

# ===================== RUNWAY MANAGEMENT PAGE =====================
def show_runway_management(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent, text="Runway Management", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

    runways = db_utils.get_all_runways()

    # Create a frame for the list
    list_frame = tk.Frame(parent, bg=CARD_COLOR, width=700, height=300)
    list_frame.pack(padx=20, pady=10, fill="both", expand=True)
    list_frame.pack_propagate(False)

    # List header
    header_frame = tk.Frame(list_frame, bg="#475569")
    header_frame.pack(fill="x", padx=10, pady=10)
    tk.Label(header_frame, text="Runway ID", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=15).pack(side="left")
    tk.Label(header_frame, text="Length (m)", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=15).pack(side="left")
    tk.Label(header_frame, text="Status", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=15).pack(side="left")
    tk.Label(header_frame, text="Actions", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=15).pack(side="left")

    # List items
    for runway in runways:
        row_frame = tk.Frame(list_frame, bg=CARD_COLOR)
        row_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(row_frame, text=runway['runway_id'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=15).pack(side="left")
        tk.Label(row_frame, text=runway['length'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=15).pack(side="left")
        
        status_color = "#22c55e" if runway['status'] == "Available" else "#ef4444"
        tk.Label(row_frame, text=runway['status'], font=("Segoe UI", 10), fg=status_color, bg=CARD_COLOR, width=15).pack(side="left")
        
        if runway['status'] == "Available":
            action_text = "Maintenance"
            new_status = "Maintenance"
        else:
            action_text = "Available"
            new_status = "Available"
        
        tk.Button(row_frame, text=action_text, bg=BTN_PRIMARY, fg="white", relief="flat", width=8,
                  command=lambda rid=runway['runway_id'], ns=new_status: update_runway_status(rid, ns, switch_page, show_runway_management, back_page, back_args)).pack(side="left", padx=5)

def update_runway_status(runway_id, new_status, switch_page, current_page, back_page, back_args):
    db_utils.update_runway_status(runway_id, new_status)
    messagebox.showinfo("Success", f"Runway {runway_id} status updated to {new_status}!")
    switch_page(current_page, back_page, back_args)

# ===================== FLIGHT SCHEDULE PAGE =====================
def show_flight_schedule(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent, text="Flight Schedule", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

    flights = db_utils.get_all_flights()

    # Create a frame for the list
    list_frame = tk.Frame(parent, bg=CARD_COLOR, width=950, height=350)
    list_frame.pack(padx=20, pady=10, fill="both", expand=True)
    list_frame.pack_propagate(False)

    # List header
    header_frame = tk.Frame(list_frame, bg="#475569")
    header_frame.pack(fill="x", padx=10, pady=10)
    tk.Label(header_frame, text="Flight", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=10).pack(side="left")
    tk.Label(header_frame, text="Airline", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=10).pack(side="left")
    tk.Label(header_frame, text="Route", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=15).pack(side="left")
    tk.Label(header_frame, text="Departure", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=12).pack(side="left")
    tk.Label(header_frame, text="Gate", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=8).pack(side="left")
    tk.Label(header_frame, text="Runway", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=8).pack(side="left")

    # List items
    for flight in flights:
        row_frame = tk.Frame(list_frame, bg=CARD_COLOR)
        row_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(row_frame, text=flight['flight_id'], font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=10).pack(side="left")
        tk.Label(row_frame, text=flight['airline_id'], font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=10).pack(side="left")
        route = f"{flight['origin']}-{flight['destination']}"
        tk.Label(row_frame, text=route, font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=15).pack(side="left")
        tk.Label(row_frame, text=flight['departure'], font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=12).pack(side="left")
        tk.Label(row_frame, text=flight['gate'], font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=8).pack(side="left")
        tk.Label(row_frame, text=flight['runway'], font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=8).pack(side="left")

# ===================== FLIGHT STATUS PAGE =====================
def show_flight_status(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent, text="Flight Status Updates", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

    flights = db_utils.get_all_flights()

    # Create a frame for the list
    list_frame = tk.Frame(parent, bg=CARD_COLOR, width=850, height=350)
    list_frame.pack(padx=20, pady=10, fill="both", expand=True)
    list_frame.pack_propagate(False)

    # List header
    header_frame = tk.Frame(list_frame, bg="#475569")
    header_frame.pack(fill="x", padx=10, pady=10)
    tk.Label(header_frame, text="Flight ID", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=12).pack(side="left")
    tk.Label(header_frame, text="Route", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=20).pack(side="left")
    tk.Label(header_frame, text="Status", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=15).pack(side="left")
    tk.Label(header_frame, text="Actions", font=("Segoe UI", 11, "bold"), fg=TEXT_COLOR, bg="#475569", width=15).pack(side="left")

    # List items
    for flight in flights:
        row_frame = tk.Frame(list_frame, bg=CARD_COLOR)
        row_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(row_frame, text=flight['flight_id'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=12).pack(side="left")
        route = f"{flight['origin']}->{flight['destination']}"
        tk.Label(row_frame, text=route, font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=20).pack(side="left")
        
        status_color = "#22c55e" if flight['status'] == "On Schedule" else "#ef4444"
        tk.Label(row_frame, text=flight['status'], font=("Segoe UI", 10), fg=status_color, bg=CARD_COLOR, width=15).pack(side="left")
        
        new_status = "Delayed" if flight['status'] == "On Schedule" else "On Schedule"
        tk.Button(row_frame, text="Change", bg=BTN_SECONDARY, fg="white", relief="flat", width=8,
                  command=lambda fid=flight['flight_id'], ns=new_status: update_flight_status(fid, ns, switch_page, show_flight_status, back_page, back_args)).pack(side="left", padx=5)

def update_flight_status(flight_id, new_status, switch_page, current_page, back_page, back_args):
    db_utils.update_flight_status(flight_id, new_status)
    messagebox.showinfo("Success", f"Flight {flight_id} status updated to {new_status}!")
    switch_page(current_page, back_page, back_args)