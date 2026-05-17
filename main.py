# main_app.py

import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from auth_module import show_passkey_page
from simulation_engine import get_sim_time, set_sim_time, update_simulation, get_time_speed, set_time_speed
import airline_module
import ticket_module
import atc_module
import checkin_module
import db_utils

# ===================== MAIN WINDOW =====================
root = tk.Tk()
root.title("Airport Management System")
root.geometry("1000x800")
root.configure(bg="#0f172a")
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))
#root.resizable(False, False)

# Top bar for global controls and clock
top_bar = tk.Frame(root, bg="#0f172a")
top_bar.pack(fill="x")
nav_button = tk.Button(top_bar,
                       text="",
                       font=("Segoe UI", 14, "bold"),
                       bg="#0f172a",
                       fg="white",
                       relief="flat")
nav_button.pack_forget()

settings_button = tk.Button(top_bar,
                            text="⚙",
                            font=("Segoe UI", 16, "bold"),
                            bg="#0f172a",
                            fg="white",
                            relief="flat",
                            command=lambda: show_settings())
settings_button.pack_forget()

clock_label = tk.Label(top_bar,
                       text="",
                       font=("Segoe UI", 14),
                       fg="#a5b4fc",
                       bg="#0f172a")
clock_label.pack(side="right", padx=20, pady=10)


def set_nav_button(text, command):
    nav_button.config(text=text, command=command)
    nav_button.pack(side="left", padx=20, pady=10)


def clear_nav_button():
    nav_button.pack_forget()

root.set_nav_button = set_nav_button
root.clear_nav_button = clear_nav_button


def refresh_clock():
    clock_label.config(text=f"Sim Time: {get_sim_time().strftime('%Y-%m-%d %H:%M')}")
    clock_label.after(1000, refresh_clock)

refresh_clock()

main_container = tk.Frame(root, bg="#0f172a")
main_container.pack(fill="both", expand=True)

current_frame = None

# ===================== PAGE SWITCH FUNCTION =====================
def switch_page(page_function, *args):
    global current_frame

    settings_button.pack_forget()
    clear_nav_button()
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

def show_settings():
    settings_win = tk.Toplevel(root)
    settings_win.title("Simulation Settings")
    settings_win.configure(bg="#0f172a")
    settings_win.geometry("450x340")
    settings_win.resizable(False, False)

    tk.Label(settings_win, text="Simulation Settings", font=("Segoe UI", 18, "bold"), fg="white", bg="#0f172a").pack(pady=(20, 10))

    content = tk.Frame(settings_win, bg="#0f172a")
    content.pack(padx=20, pady=10)

    tk.Label(content, text="Set Sim Time:", font=("Segoe UI", 11), fg="white", bg="#0f172a").grid(row=0, column=0, sticky="w", pady=10)
    current_time_var = tk.StringVar(value=get_sim_time().strftime('%Y-%m-%d %H:%M'))
    current_time_entry = tk.Entry(content, textvariable=current_time_var, width=22, font=("Segoe UI", 11), bg="#1e293b", fg="white", insertbackground="white", relief="flat")
    current_time_entry.grid(row=0, column=1, padx=15, pady=10)

    tk.Label(content, text="Growth Rate (1 sec = X min):", font=("Segoe UI", 11), fg="white", bg="#0f172a").grid(row=1, column=0, sticky="w", pady=10)
    speed_var = tk.StringVar(value=str(get_time_speed()))
    speed_options = ["1", "2", "5", "10", "15", "30"]
    speed_menu = tk.OptionMenu(content, speed_var, *speed_options)
    speed_menu.configure(font=("Segoe UI", 10), bg="#1e293b", fg="white", activebackground="#2563eb", activeforeground="white", relief="flat", highlightthickness=0, width=12)
    speed_menu["menu"].configure(bg="#1e293b", fg="white", font=("Segoe UI", 10))
    speed_menu.grid(row=1, column=1, padx=15, pady=10, sticky="w")

    def apply_settings():
        time_text = current_time_var.get().strip()
        try:
            new_time = datetime.strptime(time_text, '%Y-%m-%d %H:%M')
        except ValueError:
            messagebox.showerror("Invalid Time", "Enter time as YYYY-MM-DD HH:MM")
            return
        set_sim_time(new_time)
        try:
            new_speed = int(speed_var.get())
        except ValueError:
            messagebox.showerror("Invalid Speed", "Growth rate must be a number.")
            return
        set_time_speed(new_speed)
        clock_label.config(text=f"Sim Time: {get_sim_time().strftime('%Y-%m-%d %H:%M')}")
        messagebox.showinfo("Settings Updated", f"Sim time set and growth rate changed to 1 sec = {new_speed} min.")
        settings_win.destroy()

    apply_btn = tk.Button(settings_win, text="Apply Settings", font=("Segoe UI", 11, "bold"), bg="#2563eb", fg="white", activebackground="#1d4ed8", activeforeground="white", relief="flat", padx=25, pady=6, cursor="hand2", command=apply_settings)
    apply_btn.pack(pady=10)

    def refresh_simulation_data():
        if messagebox.askyesno("Reset Simulation Data", "Reset flights and airport status to the initial state?"):
            db_utils.reset_simulation_data()
            messagebox.showinfo("Reset Complete", "CSV data has been restored to initial simulation state.")
            settings_win.destroy()

    reset_btn = tk.Button(settings_win, text="Reset Simulation Data", font=("Segoe UI", 10, "bold"), bg="#dc2626", fg="white", activebackground="#b91c1c", activeforeground="white", relief="flat", padx=15, pady=5, cursor="hand2", command=refresh_simulation_data)
    reset_btn.pack(pady=(10, 20))


def show_home(parent, switch_page):
    settings_button.pack(side="left", padx=20, pady=10)

    tk.Label(parent,
             text="AIRPORT MANAGEMENT SYSTEM",
             font=("Segoe UI", 26, "bold"),
             fg="white",
             bg="#0f172a").pack(pady=(40, 10))

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
update_simulation(root)
root.mainloop()