# atc_module.py

import tkinter as tk

BG_COLOR = "#0f172a"

def show_atc_dashboard(parent, switch_page):

    parent.configure(bg=BG_COLOR)

    tk.Label(parent,
             text="ATC DASHBOARD",
             font=("Segoe UI", 24, "bold"),
             fg="white",
             bg=BG_COLOR).pack(pady=100)