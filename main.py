# main_app.py

import tkinter as tk
from auth_module import show_passkey_page
import airline_module
import ticket_module
import atc_module
import checkin_module

# ===================== MAIN WINDOW =====================
root = tk.Tk()
root.title("Airport Management System")
root.geometry("1000x800")
root.configure(bg="#0f172a")
#root.resizable(False, False)

main_container = tk.Frame(root, bg="#0f172a")
main_container.pack(fill="both", expand=True)

current_frame = None

# ===================== PAGE SWITCH FUNCTION =====================
def switch_page(page_function, *args):
    global current_frame

    if current_frame is not None:
        current_frame.destroy()

    current_frame = tk.Frame(main_container, bg="#0f172a")
    current_frame.pack(fill="both", expand=True)

    page_function(current_frame, switch_page, *args)

# ===================== MODULE ROUTER =====================
def route_module(module_name):

    module_routes = {
        "MANAGE AIRLINES": airline_module.show_airline_dashboard,
        "TICKET COUNTER": ticket_module.show_ticket_dashboard,
        "ATC": atc_module.show_atc_dashboard,
        "CHECKIN": checkin_module.show_checkin_dashboard
    }

    # Pass show_home into module
    switch_page(module_routes[module_name], show_home, ())
# ===================== HOME PAGE =====================



def show_home(parent, switch_page):

    tk.Label(parent,
             text="✈ AIRPORT MANAGEMENT SYSTEM",
             font=("Segoe UI", 26, "bold"),
             fg="white",
             bg="#0f172a").pack(pady=60)

    button_frame = tk.Frame(parent, bg="#0f172a")
    button_frame.pack()

    modules = [
        ("MANAGE AIRLINES", "#2563eb"),
        ("TICKET COUNTER", "#16a34a"),
        ("ATC", "#d97706"),
        ("CHECKIN", "#db2777")
    ]

    for name, color in modules:
        tk.Button(button_frame,
                  text=name,
                  font=("Segoe UI", 14, "bold"),
                  width=25,
                  height=2,
                  bg=color,
                  fg="white",
                  relief="flat",
                  command=lambda m=name: switch_page(show_passkey_page, m, route_module, show_home, ())
                  ).pack(pady=15)

# ===================== START =====================
switch_page(show_home)
root.mainloop()