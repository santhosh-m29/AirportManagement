# checkin_module.py

import tkinter as tk

BG_COLOR = "#0f172a"

def show_checkin_dashboard(parent, switch_page):

    parent.configure(bg=BG_COLOR)

    tk.Label(parent,
             text="CHECKIN DASHBOARD",
             font=("Segoe UI", 24, "bold"),
             fg="white",
             bg=BG_COLOR).pack(pady=100)