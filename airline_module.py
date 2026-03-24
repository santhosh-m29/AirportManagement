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
def create_header(parent, switch_page, show_home):
    header = tk.Frame(parent, bg=BG_COLOR)
    header.pack(fill="x", pady=10)

    tk.Button(header,
              text="Logout",
              bg=BTN_DANGER,
              fg="white",
              font=("Segoe UI", 10, "bold"),
              relief="flat",
              command=lambda: switch_page(show_home)
              ).pack(side="left", padx=20)

# ===================== MAIN DASHBOARD =====================
def show_airline_dashboard(parent, switch_page, show_home):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, show_home)

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
                  lambda: switch_page(show_edit_airlines, show_home)
                  ).pack(pady=15)

    create_option("Aircraft Information",
                  lambda: switch_page(show_aircraft_info, show_home)
                  ).pack(pady=15)

    create_option("Pilot / Crew Data",
                  lambda: switch_page(show_crew_data, show_home)
                  ).pack(pady=15)

# ===================== EDIT AIRLINES PAGE =====================
def show_edit_airlines(parent, switch_page, show_home):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, show_home)

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
                  command=lambda aid=airline['airline_id']: switch_page(show_edit_airline_form, show_home, aid)).pack(side="left", padx=5)
        tk.Button(action_frame, text="Delete", bg=BTN_DANGER, fg="white", relief="flat", width=8,
                  command=lambda aid=airline['airline_id']: delete_airline_action(aid, switch_page, show_edit_airlines, show_home)).pack(side="left", padx=5)

    # Add new airline button
    button_frame = tk.Frame(parent, bg=BG_COLOR)
    button_frame.pack(pady=20)
    tk.Button(button_frame, text="+ Add New Airline", font=("Segoe UI", 12, "bold"), bg=BTN_SUCCESS, 
              fg="white", relief="flat", command=lambda: switch_page(show_add_airline_form, show_home)).pack()

def delete_airline_action(airline_id, switch_page, current_page, show_home):
    if messagebox.askyesno("Confirm", "Are you sure you want to delete this airline?"):
        db_utils.delete_airline(airline_id)
        messagebox.showinfo("Success", "Airline deleted successfully!")
        switch_page(current_page, show_home)

def show_edit_airline_form(parent, switch_page, show_home, airline_id):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, show_home)

    airlines = db_utils.get_all_airlines()
    airline = next((a for a in airlines if a['airline_id'] == airline_id), None)

    if not airline:
        messagebox.showerror("Error", "Airline not found!")
        switch_page(show_edit_airlines, show_home)
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

    tk.Label(form_frame, text="Number of Flights:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    flights_var = tk.StringVar(value=airline['flights'])
    flights_entry = tk.Entry(form_frame, textvariable=flights_var, width=30)
    flights_entry.pack(pady=5)

    def save_changes():
        db_utils.update_airline(airline_id, name_var.get(), flights_var.get())
        messagebox.showinfo("Success", "Airline updated successfully!")
        switch_page(show_edit_airlines, show_home)

    tk.Button(form_frame, text="Save Changes", bg=BTN_SUCCESS, fg="white", relief="flat", font=("Segoe UI", 11, "bold"),
              command=save_changes).pack(pady=20)

def show_add_airline_form(parent, switch_page, show_home):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, show_home)

    tk.Label(parent, text="Add New Airline", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

    form_frame = tk.Frame(parent, bg=BG_COLOR)
    form_frame.pack(pady=20)

    tk.Label(form_frame, text="Airline ID:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w")
    id_var = tk.StringVar()
    id_entry = tk.Entry(form_frame, textvariable=id_var, width=30)
    id_entry.pack(pady=5)

    tk.Label(form_frame, text="Airline Name:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    name_var = tk.StringVar()
    name_entry = tk.Entry(form_frame, textvariable=name_var, width=30)
    name_entry.pack(pady=5)

    tk.Label(form_frame, text="Number of Flights:", font=("Segoe UI", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 0))
    flights_var = tk.StringVar(value="0")
    flights_entry = tk.Entry(form_frame, textvariable=flights_var, width=30)
    flights_entry.pack(pady=5)

    def add_airline():
        if not id_var.get() or not name_var.get():
            messagebox.showerror("Error", "All fields are required!")
            return
        db_utils.add_airline(id_var.get(), name_var.get(), flights_var.get())
        messagebox.showinfo("Success", "Airline added successfully!")
        switch_page(show_edit_airlines, show_home)

    tk.Button(form_frame, text="Add Airline", bg=BTN_SUCCESS, fg="white", relief="flat", font=("Segoe UI", 11, "bold"),
              command=add_airline).pack(pady=20)

# ===================== AIRCRAFT INFO PAGE =====================
def show_aircraft_info(parent, switch_page, show_home):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, show_home)

    tk.Label(parent, text="Aircraft Information", font=("Segoe UI", 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

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
def show_crew_data(parent, switch_page, show_home):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, show_home)

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

