# checkin_module.py

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
def show_checkin_dashboard(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent,
             text="CHECKIN DESK",
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
    
    create_option("Check-in Passenger",
                  lambda: switch_page(show_checkin_form, show_checkin_dashboard, (back_page, back_args))
                  ).pack(pady=15)

    create_option("View Baggage Info",
                  lambda: switch_page(show_baggage_info, show_checkin_dashboard, (back_page, back_args))
                  ).pack(pady=15)

    create_option("Checked-in Passengers",
                  lambda: switch_page(show_checkedin_passengers, show_checkin_dashboard, (back_page, back_args))
                  ).pack(pady=15)

# ===================== CHECK-IN FORM PAGE =====================
def show_checkin_form(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent, text="Passenger Check-in", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

    form_frame = tk.Frame(parent, bg=BG_COLOR)
    form_frame.pack(pady=20)

    tk.Label(form_frame, text="Passenger ID:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w")
    passenger_id_var = tk.StringVar()
    passenger_id_entry = tk.Entry(form_frame, textvariable=passenger_id_var, width=30)
    passenger_id_entry.pack(pady=5)
    passenger_id_entry.bind("<Return>", lambda e: process_checkin())

    tk.Label(form_frame, text="Baggage Weight (kg):", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    baggage_var = tk.StringVar(value="0")
    baggage_entry = tk.Entry(form_frame, textvariable=baggage_var, width=30)
    baggage_entry.pack(pady=5)
    baggage_entry.bind("<Return>", lambda e: process_checkin())

    def process_checkin():
        if not passenger_id_var.get():
            messagebox.showerror("Error", "Passenger ID is required!")
            return
        
        try:
            baggage = float(baggage_var.get())
        except ValueError:
            messagebox.showerror("Error", "Baggage weight must be a number!")
            return
        
        if baggage > 25:
            messagebox.showerror("Error", "Baggage weight exceeds 25kg limit!")
            return
        
        # Find and update passenger
        passengers = db_utils.get_all_passengers()
        passenger = next((p for p in passengers if p['passenger_id'] == passenger_id_var.get()), None)
        
        if not passenger:
            messagebox.showerror("Error", "Passenger not found!")
            return
        
        db_utils.update_passenger_checkin(passenger_id_var.get(), "Yes", str(baggage))
        messagebox.showinfo("Success", f"Passenger {passenger['name']} checked in successfully!\nBaggage: {baggage}kg")
        switch_page(back_page, *back_args)

    tk.Button(form_frame, text="Process Check-in", bg=BTN_SUCCESS, fg="white", relief="flat", font=("Segoe UI", 11, "bold"),
              command=process_checkin).pack(pady=20)

# ===================== BAGGAGE INFO PAGE =====================
def show_baggage_info(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent, text="Baggage Information", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

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
    tk.Label(header_frame, text="Baggage (kg)", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=12).pack(side="left")
    tk.Label(header_frame, text="Status", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=12).pack(side="left")

    # List items
    for passenger in passengers:
        row_frame = tk.Frame(list_frame, bg=CARD_COLOR)
        row_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(row_frame, text=passenger['passenger_id'], font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=15).pack(side="left")
        tk.Label(row_frame, text=passenger['name'], font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=15).pack(side="left")
        tk.Label(row_frame, text=passenger['baggage_weight'], font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=12).pack(side="left")
        
        status_color = "#22c55e" if passenger['checked_in'] == "Yes" else "#ef4444"
        tk.Label(row_frame, text=passenger['checked_in'], font=("Segoe UI", 9), fg=status_color, bg=CARD_COLOR, width=12).pack(side="left")

# ===================== CHECKED-IN PASSENGERS PAGE =====================
def show_checkedin_passengers(parent, switch_page, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)

    tk.Label(parent, text="Checked-in Passengers", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

    passengers = db_utils.get_all_passengers()
    checkedin = [p for p in passengers if p['checked_in'] == "Yes"]

    # Create a frame for the list
    list_frame = tk.Frame(parent, bg=CARD_COLOR, width=900, height=350)
    list_frame.pack(padx=20, pady=10, fill="both", expand=True)
    list_frame.pack_propagate(False)

    if not checkedin:
        tk.Label(list_frame, text="No passengers checked in yet.", font=("Segoe UI", 12), fg=SUB_TEXT, bg=CARD_COLOR).pack(pady=150)
    else:
        # List header
        header_frame = tk.Frame(list_frame, bg="#475569")
        header_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(header_frame, text="Passenger ID", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=15).pack(side="left")
        tk.Label(header_frame, text="Name", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=15).pack(side="left")
        tk.Label(header_frame, text="Flight ID", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=12).pack(side="left")
        tk.Label(header_frame, text="Seat", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=10).pack(side="left")
        tk.Label(header_frame, text="Baggage", font=("Segoe UI", 10, "bold"), fg=TEXT_COLOR, bg="#475569", width=10).pack(side="left")

        # List items
        for passenger in checkedin:
            row_frame = tk.Frame(list_frame, bg=CARD_COLOR)
            row_frame.pack(fill="x", padx=10, pady=5)
            tk.Label(row_frame, text=passenger['passenger_id'], font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=15).pack(side="left")
            tk.Label(row_frame, text=passenger['name'], font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=15).pack(side="left")
            tk.Label(row_frame, text=passenger['flight_id'], font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=12).pack(side="left")
            tk.Label(row_frame, text=passenger['seat'], font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=10).pack(side="left")
            tk.Label(row_frame, text=f"{passenger['baggage_weight']}kg", font=("Segoe UI", 9), fg=TEXT_COLOR, bg=CARD_COLOR, width=10).pack(side="left")