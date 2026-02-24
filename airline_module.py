# airline_module.py

import tkinter as tk
# airline_module.py

import tkinter as tk
from tkinter import messagebox

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

    # Logout (Top Left)
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

    tk.Label(parent,
             text="MANAGE AIRLINES DASHBOARD",
             font=("Segoe UI", 24, "bold"),
             fg="white",
             bg=BG_COLOR).pack(pady=100)

    tk.Button(parent,
              text="Back to Home",
              command=lambda: switch_page(show_home)
              ).pack()
    
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
             bg=BG_COLOR).pack(pady=40)

    card = tk.Frame(parent, bg=CARD_COLOR, width=500, height=300)
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    tk.Label(card,
             text="Airline Name",
             bg=CARD_COLOR,
             fg=TEXT_COLOR).pack(pady=10)

    tk.Entry(card, width=30).pack()

    tk.Button(card,
              text="Save Changes",
              bg=BTN_SUCCESS,
              fg="white",
              relief="flat").pack(pady=20)


# ===================== AIRCRAFT INFO PAGE =====================
def show_aircraft_info(parent, switch_page, show_home):

    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, show_home)

    tk.Label(parent,
             text="Aircraft Information",
             font=("Segoe UI", 22, "bold"),
             fg=TEXT_COLOR,
             bg=BG_COLOR).pack(pady=40)

    tk.Label(parent,
             text="Aircraft data management UI will be implemented here.",
             fg=SUB_TEXT,
             bg=BG_COLOR).pack()


# ===================== CREW DATA PAGE =====================
def show_crew_data(parent, switch_page, show_home):

    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, show_home)

    tk.Label(parent,
             text="Pilot / Crew Data",
             font=("Segoe UI", 22, "bold"),
             fg=TEXT_COLOR,
             bg=BG_COLOR).pack(pady=40)

    tk.Label(parent,
             text="Crew management UI will be implemented here.",
             fg=SUB_TEXT,
             bg=BG_COLOR).pack()

