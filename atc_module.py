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

    root = parent.winfo_toplevel()
    if back_page:
        root.set_nav_button("Back", lambda: switch_page(back_page, *back_args))

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
    container = tk.Frame(parent, bg=CARD_COLOR, width=850, height=350)
    container.pack(padx=20, pady=10, fill="both", expand=True)
    container.pack_propagate(False)

    canvas = tk.Canvas(container, bg=CARD_COLOR, highlightthickness=0, width=850, height=350)
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
    tk.Label(header_frame, text="Gate ID", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=18).pack(side="left")
    tk.Label(header_frame, text="Terminal", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=22).pack(side="left")
    tk.Label(header_frame, text="Status", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=22).pack(side="left")
    tk.Label(header_frame, text="Actions", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=20).pack(side="left")

    # List items
    for gate in gates:
        row_frame = tk.Frame(list_frame, bg=CARD_COLOR)
        row_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(row_frame, text=gate['gate_id'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=18).pack(side="left")
        tk.Label(row_frame, text=gate['terminal'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=22).pack(side="left")
        normalized_status = gate.get('status', '').strip().lower()
        display_status = "Available" if normalized_status == "available" else "Not Available"
        status_color = "#22c55e" if normalized_status == "available" else "#ef4444"
        tk.Label(row_frame, text=display_status, font=("Segoe UI", 10), fg=status_color, bg=CARD_COLOR, width=22).pack(side="left")

        toggle_status = "OCCUPIED" if normalized_status == "available" else "AVAILABLE"
        btn_text = "Mark Occupied" if normalized_status == "available" else "Mark Available"
        btn_color = "#ef4444" if normalized_status == "available" else "#22c55e"
        tk.Button(row_frame,
                  text=btn_text,
                  font=("Segoe UI", 9, "bold"),
                  bg=btn_color,
                  fg="white",
                  relief="flat",
                  width=18,
                  cursor="hand2",
                  command=lambda gid=gate['gate_id'], ts=toggle_status: update_gate_status(gid, ts, switch_page, show_gate_management, back_page, back_args)
                  ).pack(side="left", padx=5)

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

    # Create a frame for the list (scrollable)
    container = tk.Frame(parent, bg=CARD_COLOR, width=850, height=300)
    container.pack(padx=20, pady=10, fill="both", expand=True)
    container.pack_propagate(False)

    canvas = tk.Canvas(container, bg=CARD_COLOR, highlightthickness=0, width=850, height=300)
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
    tk.Label(header_frame, text="Runway ID", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=22).pack(side="left")
    tk.Label(header_frame, text="Length (m)", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=22).pack(side="left")
    tk.Label(header_frame, text="Status", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=22).pack(side="left")
    tk.Label(header_frame, text="Actions", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=20).pack(side="left")

    # List items
    for runway in runways:
        row_frame = tk.Frame(list_frame, bg=CARD_COLOR)
        row_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(row_frame, text=runway['runway_id'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=22).pack(side="left")
        tk.Label(row_frame, text=runway['length'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=22).pack(side="left")
        
        normalized_status = runway.get('status', '').strip().lower()
        display_status = "Available" if normalized_status == "available" else "Not Available"
        status_color = "#22c55e" if normalized_status == "available" else "#ef4444"
        tk.Label(row_frame, text=display_status, font=("Segoe UI", 10), fg=status_color, bg=CARD_COLOR, width=22).pack(side="left")

        toggle_status = "OCCUPIED" if normalized_status == "available" else "AVAILABLE"
        btn_text = "Mark Occupied" if normalized_status == "available" else "Mark Available"
        btn_color = "#ef4444" if normalized_status == "available" else "#22c55e"
        tk.Button(row_frame,
                  text=btn_text,
                  font=("Segoe UI", 9, "bold"),
                  bg=btn_color,
                  fg="white",
                  relief="flat",
                  width=18,
                  cursor="hand2",
                  command=lambda rid=runway['runway_id'], ts=toggle_status: update_runway_status(rid, ts, switch_page, show_runway_management, back_page, back_args)
                  ).pack(side="left", padx=5)

def update_runway_status(runway_id, new_status, switch_page, current_page, back_page, back_args):
    db_utils.update_runway_status(runway_id, new_status)
    messagebox.showinfo("Success", f"Runway {runway_id} status updated to {new_status}!")
    switch_page(current_page, back_page, back_args)

# ===================== FLIGHT SCHEDULE PAGE =====================
def show_flight_schedule(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent, text="Flight Schedule", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

    # Create a frame for the list (scrollable)
    container = tk.Frame(parent, bg=CARD_COLOR, width=1150, height=350)
    container.pack(padx=20, pady=10, fill="both", expand=True)
    container.pack_propagate(False)

    canvas = tk.Canvas(container, bg=CARD_COLOR, highlightthickness=0, width=1150, height=350)
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
    tk.Label(header_frame, text="Flight", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=12).pack(side="left")
    tk.Label(header_frame, text="Airline", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=12).pack(side="left")
    tk.Label(header_frame, text="Route", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=16).pack(side="left")
    tk.Label(header_frame, text="Departure", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=12).pack(side="left")
    tk.Label(header_frame, text="Arrival", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=12).pack(side="left")
    tk.Label(header_frame, text="Gate/Runway", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=16).pack(side="left")
    tk.Label(header_frame, text="Status", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=14).pack(side="left")
    tk.Label(header_frame, text="Flight Progress", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=25).pack(side="left")

    rows_container = tk.Frame(list_frame, bg=CARD_COLOR)
    rows_container.pack(fill="both", expand=True)

    def refresh_rows():
        if not rows_container.winfo_exists():
            return

        # Clear old rows
        for child in rows_container.winfo_children():
            child.destroy()

        flights = db_utils.get_all_flights()
        import simulation_engine

        current_time_str = simulation_engine.SIM_TIME.strftime("%H:%M")
        
        def _parse_time(t_str):
            try:
                h, m = map(int, t_str.split(':'))
                return h * 60 + m
            except Exception:
                return 0

        c_mins = _parse_time(current_time_str)

        for flight in flights:
            row_frame = tk.Frame(rows_container, bg=CARD_COLOR)
            row_frame.pack(fill="x", padx=10, pady=5)

            tk.Label(row_frame, text=flight['flight_id'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=12).pack(side="left")
            tk.Label(row_frame, text=flight['airline_id'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=12).pack(side="left")
            route = f"{flight['origin']}->{flight['destination']}"
            tk.Label(row_frame, text=route, font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=16).pack(side="left")
            
            dep = flight.get('departure_time') or flight.get('departure')
            arr = flight.get('arrival_time') or flight.get('arrival')
            tk.Label(row_frame, text=dep, font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=12).pack(side="left")
            tk.Label(row_frame, text=arr, font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=12).pack(side="left")
            
            gate_rw = f"G: {flight.get('gate') or '-'} | R: {flight.get('runway') or '-'}"
            tk.Label(row_frame, text=gate_rw, font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=16).pack(side="left")

            status = flight.get('status', '').upper()
            status_color = "#22c55e" if status in ["BOARDING", "CHECK-IN OPEN", "TAXIING", "IN AIR"] else ("#3b82f6" if status == "ARRIVED" else "#ef4444")
            tk.Label(row_frame, text=status, font=("Segoe UI", 10, "bold"), fg=status_color, bg=CARD_COLOR, width=14).pack(side="left")

            # Progress percentage
            if status in ["SCHEDULED", "CHECK-IN OPEN", "BOARDING", "GATE CLOSED", "CANCELLED"]:
                progress = 0.0
            elif status == "ARRIVED":
                progress = 1.0
            else:
                d_mins = _parse_time(dep)
                a_mins = _parse_time(arr)
                if a_mins > d_mins:
                    # Same-day flight
                    if c_mins <= d_mins:
                        progress = 0.0
                    elif c_mins >= a_mins:
                        progress = 1.0
                    else:
                        progress = (c_mins - d_mins) / (a_mins - d_mins)
                else:
                    # Overnight flight
                    total_duration = (24 * 60 - d_mins) + a_mins
                    if c_mins >= d_mins:
                        progress = (c_mins - d_mins) / total_duration
                    elif c_mins <= a_mins:
                        progress = ((24 * 60 - d_mins) + c_mins) / total_duration
                    else:
                        progress = 1.0 if c_mins < d_mins and c_mins > a_mins else 0.0

            # Build visual progress bar
            progress_frame = tk.Frame(row_frame, bg=CARD_COLOR, width=200, height=25)
            progress_frame.pack(side="left", padx=5)
            progress_frame.pack_propagate(False)

            progress_canvas = tk.Canvas(progress_frame, bg=CARD_COLOR, highlightthickness=0, width=200, height=25)
            progress_canvas.pack(fill="both", expand=True)

            # Track
            progress_canvas.create_line(10, 12, 160, 12, fill="#334155", width=4)

            # Active line
            active_width = 10 + int(progress * 150)
            if progress > 0:
                progress_canvas.create_line(10, 12, active_width, 12, fill="#3b82f6" if progress < 1.0 else "#22c55e", width=4)

            # Icon
            icon_color = "#3b82f6" if progress < 1.0 else "#22c55e"
            if progress >= 1.0:
                progress_canvas.create_oval(active_width - 4, 8, active_width + 4, 16, fill="#22c55e", outline="#22c55e")
            elif status == "CANCELLED":
                progress_canvas.create_oval(6, 8, 14, 16, fill="#ef4444", outline="#ef4444")
            elif progress > 0:
                progress_canvas.create_text(active_width, 12, text="✈", fill=icon_color, font=("Segoe UI", 11, "bold"))
            else:
                progress_canvas.create_oval(6, 8, 14, 16, fill="#64748b", outline="#64748b")

            # Percentage label
            percentage_str = f"{int(progress * 100)}%" if status != "CANCELLED" else "N/A"
            progress_canvas.create_text(170, 12, text=percentage_str, fill=SUB_TEXT, font=("Segoe UI", 8, "bold"), anchor="w")

        # Refresh every second
        rows_container.after(1000, refresh_rows)

    refresh_rows()

# ===================== FLIGHT STATUS PAGE =====================
def show_flight_status(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent, text="Flight Status Updates", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

    flights = db_utils.get_all_flights()

    # Create a frame for the list (scrollable)
    container = tk.Frame(parent, bg=CARD_COLOR, width=1000, height=350)
    container.pack(padx=20, pady=10, fill="both", expand=True)
    container.pack_propagate(False)

    canvas = tk.Canvas(container, bg=CARD_COLOR, highlightthickness=0, width=1000, height=350)
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
    tk.Label(header_frame, text="Flight ID", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=18).pack(side="left")
    tk.Label(header_frame, text="Route", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=28).pack(side="left")
    tk.Label(header_frame, text="Status", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=28).pack(side="left")
    tk.Label(header_frame, text="Manual Override", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=24).pack(side="left")

    # List items
    for flight in flights:
        row_frame = tk.Frame(list_frame, bg=CARD_COLOR)
        row_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(row_frame, text=flight['flight_id'], font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=18).pack(side="left")
        route = f"{flight['origin']}->{flight['destination']}"
        tk.Label(row_frame, text=route, font=("Segoe UI", 10), fg=TEXT_COLOR, bg=CARD_COLOR, width=28).pack(side="left")
        
        status = flight.get('status', '')
        status_color = "#22c55e" if status.upper() in ["ON SCHEDULE", "BOARDING", "CHECK-IN OPEN", "TAXIING", "IN AIR", "DEPARTED", "ARRIVED"] else "#ef4444"
        
        status_label = tk.Label(row_frame, text=status, font=("Segoe UI", 10), fg=status_color, bg=CARD_COLOR, width=28)
        status_label.pack(side="left")

        # Menu override options
        override_var = tk.StringVar(value=status)
        statuses = ["SCHEDULED", "CHECK-IN OPEN", "BOARDING", "GATE CLOSED", "TAXIING", "DEPARTED", "IN AIR", "ARRIVED", "DELAYED", "CANCELLED"]
        
        def make_update_command(fid, var):
            return lambda val: update_flight_status(fid, val, switch_page, show_flight_status, back_page, back_args)
            
        opt = tk.OptionMenu(row_frame, override_var, *statuses, command=make_update_command(flight['flight_id'], override_var))
        opt.configure(font=("Segoe UI", 9, "bold"), bg="#1e293b", fg=TEXT_COLOR, activebackground=BTN_PRIMARY, activeforeground="white", relief="flat", highlightthickness=0, width=16)
        opt["menu"].configure(bg="#1e293b", fg=TEXT_COLOR, activebackground=BTN_PRIMARY, activeforeground="white")
        opt.pack(side="left", padx=5)

def update_flight_status(flight_id, new_status, switch_page, current_page, back_page, back_args):
    db_utils.update_flight_status(flight_id, new_status)
    messagebox.showinfo("Success", f"Flight {flight_id} status updated to {new_status}!")
    switch_page(current_page, back_page, back_args)