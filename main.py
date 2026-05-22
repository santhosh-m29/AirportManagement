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
from airport_settings import (
    load_settings, save_settings, get_airport, set_airport, get_crew_rest_time,
    get_fueling_time, get_checkin_threshold, is_auto_checkin_enabled, set_auto_checkin
)

# ===================== PREMIUM DESIGN SYSTEM =====================
BG_COLOR = "#0f172a"
CARD_COLOR = "#1e293b"
BORDER_COLOR = "#243249"
TEXT_COLOR = "#f8fafc"
SUB_TEXT = "#94a3b8"
ACCENT_COLOR = "#4f46e5"
ACCENT_HOVER = "#6366f1"
BTN_SUCCESS = "#10b981"
SUCCESS_HOVER = "#34d399"
BTN_DANGER = "#f43f5e"
DANGER_HOVER = "#fb7185"

def add_hover(widget, hover_bg, normal_bg, hover_fg=None, normal_fg=None):
    def on_enter(e):
        widget.config(bg=hover_bg)
        if hover_fg and hasattr(widget, 'config'):
            try:
                widget.config(fg=hover_fg)
            except Exception:
                pass
    def on_leave(e):
        widget.config(bg=normal_bg)
        if normal_fg and hasattr(widget, 'config'):
            try:
                widget.config(fg=normal_fg)
            except Exception:
                pass
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

# ===================== MAIN WINDOW =====================
root = tk.Tk()
root.title("Airport Management System")
root.geometry("1100x850")
root.configure(bg=BG_COLOR)
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

# Top bar for global controls
top_bar = tk.Frame(root, bg=BG_COLOR, pady=10)
top_bar.pack(fill="x")

nav_button = tk.Button(top_bar,
                       text="",
                       font=("Segoe UI", 12, "bold"),
                       bg=BG_COLOR,
                       fg=TEXT_COLOR,
                       activebackground="#1e293b",
                       activeforeground=TEXT_COLOR,
                       relief="flat",
                       cursor="hand2")
nav_button.pack_forget()
add_hover(nav_button, "#1e293b", BG_COLOR)

settings_button = tk.Button(top_bar,
                            text="⚙ Settings",
                            font=("Segoe UI", 12, "bold"),
                            bg=BG_COLOR,
                            fg=TEXT_COLOR,
                            activebackground="#1e293b",
                            activeforeground=TEXT_COLOR,
                            relief="flat",
                            cursor="hand2",
                            command=lambda: show_settings())
settings_button.pack_forget()
add_hover(settings_button, "#1e293b", BG_COLOR)

close_button = tk.Button(top_bar,
                         text="Exit App",
                         font=("Segoe UI", 12, "bold"),
                         bg=BTN_DANGER,
                         fg="white",
                         relief="flat",
                         activebackground=DANGER_HOVER,
                         activeforeground="white",
                         padx=15,
                         pady=5,
                         command=root.destroy,
                         cursor="hand2")
close_button.pack_forget()
add_hover(close_button, DANGER_HOVER, BTN_DANGER)

bottom_bar = tk.Frame(root, bg=BG_COLOR)
bottom_bar.pack(side="bottom", fill="x")

clock_label = tk.Label(bottom_bar,
                       text=f"Simulation Clock: {get_sim_time().strftime('%Y-%m-%d %H:%M')} | Airport: {get_airport()}",
                       font=("Segoe UI", 12, "bold"),
                       fg=SUB_TEXT,
                       bg=BG_COLOR)
clock_label.pack(side="left", padx=30, pady=15)


def set_nav_button(text, command):
    nav_button.config(text=f"← {text}", command=command)
    nav_button.pack(side="left", padx=20, pady=10)


def clear_nav_button():
    nav_button.pack_forget()

root.set_nav_button = set_nav_button
root.clear_nav_button = clear_nav_button


def refresh_clock():
    clock_label.config(text=f"Simulation Clock: {get_sim_time().strftime('%Y-%m-%d %H:%M')} | Airport: {get_airport()}")
    clock_label.after(1000, refresh_clock)

refresh_clock()

main_container = tk.Frame(root, bg=BG_COLOR)
main_container.pack(fill="both", expand=True)

scroll_canvas = tk.Canvas(main_container, bg=BG_COLOR, highlightthickness=0)
scrollbar = tk.Scrollbar(main_container, orient="vertical", command=scroll_canvas.yview)
scroll_canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
scroll_canvas.pack(side="left", fill="both", expand=True)

scrollable_area = tk.Frame(scroll_canvas, bg=BG_COLOR)
scroll_window = scroll_canvas.create_window((0, 0), window=scrollable_area, anchor="nw")


def on_scrollable_configure(event):
    scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))


def on_canvas_configure(event):
    scroll_canvas.itemconfig(scroll_window, width=event.width)


scrollable_area.bind("<Configure>", on_scrollable_configure)
scroll_canvas.bind("<Configure>", on_canvas_configure)


def on_mousewheel(event):
    if event.delta:
        scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    elif event.num == 5:
        scroll_canvas.yview_scroll(1, "units")
    elif event.num == 4:
        scroll_canvas.yview_scroll(-1, "units")


root.bind_all("<MouseWheel>", on_mousewheel)
root.bind_all("<Button-4>", on_mousewheel)
root.bind_all("<Button-5>", on_mousewheel)

current_frame = None

# ===================== PAGE SWITCH FUNCTION =====================
def switch_page(page_function, *args):
    global current_frame

    settings_button.pack_forget()
    close_button.pack_forget()
    clear_nav_button()
    if current_frame is not None:
        current_frame.destroy()

    current_frame = tk.Frame(scrollable_area, bg=BG_COLOR)
    current_frame.pack(fill="x", expand=True)

    page_function(current_frame, switch_page, *args)

    scroll_canvas.update_idletasks()
    scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

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



# ===================== SETTINGS PANEL =====================
def show_settings():
    settings_win = tk.Toplevel(root)
    settings_win.title("Airport Management Settings")
    settings_win.configure(bg=BG_COLOR)
    settings_win.geometry("600x700")
    settings_win.resizable(False, False)

    tk.Label(settings_win, text="System Configuration Center", font=("Segoe UI", 18, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=(20, 15))

    # Create scrollable frame for settings
    canvas = tk.Canvas(settings_win, bg=BG_COLOR, highlightthickness=0)
    scrollbar = tk.Scrollbar(settings_win, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True, padx=10)

    content = tk.Frame(canvas, bg=BG_COLOR)
    canvas.create_window((0, 0), window=content, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    content.bind("<Configure>", on_frame_configure)

    # ===== SIMULATION SETTINGS =====
    tk.Label(content, text="Simulation Control", font=("Segoe UI", 13, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 10), padx=20)

    tk.Label(content, text="Set Simulation Time:", font=("Segoe UI", 10), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(10, 5), padx=20)
    current_time_var = tk.StringVar(value=get_sim_time().strftime('%Y-%m-%d %H:%M'))
    entry_frame = tk.Frame(content, bg=BORDER_COLOR, padx=1, pady=1)
    entry_frame.pack(anchor="w", padx=20, pady=5)
    current_time_entry = tk.Entry(entry_frame, textvariable=current_time_var, width=25, font=("Segoe UI", 10), bg="#111827", fg="white", insertbackground="white", relief="flat")
    current_time_entry.pack(padx=2, pady=2)

    tk.Label(content, text="Growth Rate (1 sec = X min):", font=("Segoe UI", 10), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(15, 5), padx=20)
    speed_var = tk.StringVar(value=str(get_time_speed()))
    speed_options = ["1", "2", "5", "10", "15", "30"]
    speed_menu = tk.OptionMenu(content, speed_var, *speed_options)
    speed_menu.configure(font=("Segoe UI", 10, "bold"), bg="#111827", fg=TEXT_COLOR, activebackground=ACCENT_COLOR, activeforeground="white", relief="flat", highlightthickness=0, width=20)
    speed_menu["menu"].configure(bg="#111827", fg=TEXT_COLOR, font=("Segoe UI", 10), activebackground=ACCENT_COLOR, activeforeground="white", relief="flat")
    speed_menu.pack(anchor="w", padx=20, pady=5)

    # ===== AIRPORT SETTINGS =====
    tk.Label(content, text="Airport Configuration", font=("Segoe UI", 13, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 10), padx=20)

    tk.Label(content, text="Current Airport:", font=("Segoe UI", 10), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(10, 5), padx=20)
    airport_var = tk.StringVar(value=get_airport())
    airport_options = ["Chennai", "Dubai", "Paris", "London", "New York", "Sydney", "Bangkok", "Singapore", "Tokyo", "Hong Kong"]
    airport_menu = tk.OptionMenu(content, airport_var, *airport_options)
    airport_menu.configure(font=("Segoe UI", 10, "bold"), bg="#111827", fg=TEXT_COLOR, activebackground=ACCENT_COLOR, activeforeground="white", relief="flat", highlightthickness=0, width=20)
    airport_menu["menu"].configure(bg="#111827", fg=TEXT_COLOR, font=("Segoe UI", 10), activebackground=ACCENT_COLOR, activeforeground="white", relief="flat")
    airport_menu.pack(anchor="w", padx=20, pady=5)

    # ===== OPERATIONAL SETTINGS =====
    tk.Label(content, text="Operational Settings", font=("Segoe UI", 13, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(20, 10), padx=20)

    tk.Label(content, text="Crew Rest Time (minutes):", font=("Segoe UI", 10), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(10, 5), padx=20)
    crew_rest_var = tk.StringVar(value=str(get_crew_rest_time()))
    crew_rest_entry = tk.Entry(content, textvariable=crew_rest_var, width=25, font=("Segoe UI", 10), bg="#111827", fg="white", insertbackground="white", relief="flat")
    crew_rest_entry.pack(anchor="w", padx=20, pady=5)

    tk.Label(content, text="Fueling Time (minutes):", font=("Segoe UI", 10), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(10, 5), padx=20)
    fueling_var = tk.StringVar(value=str(get_fueling_time()))
    fueling_entry = tk.Entry(content, textvariable=fueling_var, width=25, font=("Segoe UI", 10), bg="#111827", fg="white", insertbackground="white", relief="flat")
    fueling_entry.pack(anchor="w", padx=20, pady=5)

    tk.Label(content, text="Check-in Threshold (%):", font=("Segoe UI", 10), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(10, 5), padx=20)
    checkin_var = tk.StringVar(value=str(get_checkin_threshold()))
    checkin_entry = tk.Entry(content, textvariable=checkin_var, width=25, font=("Segoe UI", 10), bg="#111827", fg="white", insertbackground="white", relief="flat")
    checkin_entry.pack(anchor="w", padx=20, pady=5)

    # ===== AUTO CHECK-IN =====
    auto_checkin_var = tk.BooleanVar(value=is_auto_checkin_enabled())
    auto_checkin_check = tk.Checkbutton(content, text="Enable Auto Check-in", font=("Segoe UI", 10), fg=TEXT_COLOR, bg=BG_COLOR, activebackground=BG_COLOR, activeforeground=TEXT_COLOR, selectcolor=ACCENT_COLOR, variable=auto_checkin_var)
    auto_checkin_check.pack(anchor="w", padx=20, pady=(15, 20))

    # ===== BUTTONS =====
    button_frame = tk.Frame(content, bg=BG_COLOR)
    button_frame.pack(pady=20, padx=20, fill="x")

    def apply_settings():
        try:
            # Validate time
            time_text = current_time_var.get().strip()
            try:
                new_time = datetime.strptime(time_text, '%Y-%m-%d %H:%M')
            except ValueError:
                messagebox.showerror("Invalid Time", "Enter time as YYYY-MM-DD HH:MM")
                return
            
            # Validate speed
            try:
                new_speed = int(speed_var.get())
            except ValueError:
                messagebox.showerror("Invalid Speed", "Growth rate must be a number.")
                return
            
            # Validate operational settings
            try:
                crew_rest = int(crew_rest_var.get())
                fueling_time = int(fueling_var.get())
                checkin_thresh = int(checkin_var.get())
                if crew_rest < 0 or fueling_time < 0 or checkin_thresh < 0:
                    messagebox.showerror("Invalid Values", "All values must be positive.")
                    return
            except ValueError:
                messagebox.showerror("Invalid Values", "Operational settings must be numbers.")
                return
            
            # Apply settings
            set_sim_time(new_time)
            set_time_speed(new_speed)
            set_airport(airport_var.get())
            set_auto_checkin(auto_checkin_var.get())
            
            # Save to settings file
            settings = load_settings()
            settings['crew_rest_time'] = crew_rest
            settings['fueling_time'] = fueling_time
            settings['checkin_threshold'] = checkin_thresh
            save_settings(settings)
            
            clock_label.config(text=f"Simulation Clock: {get_sim_time().strftime('%Y-%m-%d %H:%M')} | Airport: {airport_var.get()}")
            messagebox.showinfo("Settings Updated", "All settings have been applied successfully!")
            settings_win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    apply_btn = tk.Button(button_frame, text="Apply Settings", font=("Segoe UI", 11, "bold"), bg=BTN_SUCCESS, fg="white", activebackground=SUCCESS_HOVER, activeforeground="white", relief="flat", padx=25, pady=8, cursor="hand2", command=apply_settings)
    apply_btn.pack(fill="x", pady=5)
    add_hover(apply_btn, SUCCESS_HOVER, BTN_SUCCESS)

    def refresh_simulation_data():
        if messagebox.askyesno("Reset Simulation Data", "Reset flights and airport status to the initial state?"):
            db_utils.reset_simulation_data()
            messagebox.showinfo("Reset Complete", "CSV data has been restored to initial simulation state.")
            settings_win.destroy()

    reset_btn = tk.Button(button_frame, text="Reset Database", font=("Segoe UI", 11, "bold"), bg=BTN_DANGER, fg="white", activebackground=DANGER_HOVER, activeforeground="white", relief="flat", padx=25, pady=8, cursor="hand2", command=refresh_simulation_data)
    reset_btn.pack(fill="x", pady=5)
    add_hover(reset_btn, DANGER_HOVER, BTN_DANGER)

# ===================== HOME PAGE =====================
def show_home(parent, switch_page):
    settings_button.pack(side="left", padx=20, pady=10)
    close_button.pack(side="right", padx=20, pady=10)

    # Hero Titles
    tk.Label(parent,
             text="AIRPORT CONTROL PANEL",
             font=("Segoe UI", 26, "bold"),
             fg=TEXT_COLOR,
             bg=BG_COLOR).pack(pady=(45, 5))

    tk.Label(parent,
             text="Select a management module below to view live data and adjust configurations.",
             font=("Segoe UI", 11),
             fg=SUB_TEXT,
             bg=BG_COLOR).pack(pady=(0, 30))

    cards_container = tk.Frame(parent, bg=BG_COLOR)
    cards_container.pack(pady=10)

    # 2x2 Grid setup
    modules_data = [
        ("MANAGE AIRLINES", "MANAGE AIRLINES", "✈", "Fleet, Flights & Crews", "Manage airline details, flight schedules, and crew rosters.", "#3b82f6", 0, 0),
        ("TICKET COUNTER", "TICKET COUNTER", "🎫", "Booking & Boarding Passes", "Purchase tickets, view routes and boarding passes.", "#10b981", 0, 1),
        ("ATC OPERATIONS", "ATC", "📡", "Gates & Runways Control", "Monitor runway, gates, and update flight statuses.", "#f59e0b", 1, 0),
        ("CHECK-IN COUNTER", "CHECKIN", "🧳", "Passenger Baggage & Check-in", "Verify passenger, baggage, and boarding passes.", "#8b5cf6", 1, 1)
    ]

    for display_name, module_key, icon, subtitle, desc, color, row, col in modules_data:
        # Create card frame
        card = tk.Frame(cards_container, bg=CARD_COLOR, bd=1, highlightbackground=BORDER_COLOR, highlightthickness=1, width=350, height=240)
        card.grid(row=row, column=col, padx=25, pady=20)
        card.pack_propagate(False)

        # Accent top line
        accent_bar = tk.Frame(card, bg=color, height=4)
        accent_bar.pack(fill="x", side="top")

        # Icon
        tk.Label(card, text=icon, font=("Segoe UI", 36), fg=color, bg=CARD_COLOR).pack(pady=(15, 0))

        # Title
        tk.Label(card, text=display_name, font=("Segoe UI", 14, "bold"), fg=TEXT_COLOR, bg=CARD_COLOR).pack(pady=(5, 0))

        # Subtitle
        tk.Label(card, text=subtitle, font=("Segoe UI", 9, "italic"), fg=color, bg=CARD_COLOR).pack()

        # Description
        tk.Label(card, text=desc, font=("Segoe UI", 9), fg=SUB_TEXT, bg=CARD_COLOR, wraplength=310, justify="center").pack(pady=(10, 0))

        # Launch Button Frame to hold it at the bottom
        btn_frame = tk.Frame(card, bg=CARD_COLOR)
        btn_frame.pack(side="bottom", fill="x", pady=15)

        btn = tk.Button(btn_frame,
                        text="Launch Console",
                        font=("Segoe UI", 10, "bold"),
                        bg=color,
                        fg="white",
                        relief="flat",
                        padx=20,
                        pady=5,
                        cursor="hand2",
                        activebackground=color,
                        command=lambda m=module_key: switch_page(show_passkey_page, m, route_module, show_home, ()))
        btn.pack()
        
        # Hover animation (glow white on hover)
        add_hover(btn, "#ffffff", color, hover_fg=color, normal_fg="#ffffff")

# ===================== START =====================
switch_page(show_home)
update_simulation(root)
root.mainloop()