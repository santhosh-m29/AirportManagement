# auth_module.py

import tkinter as tk
from tkinter import messagebox

BG_COLOR = "#0f172a"
CARD_COLOR = "#1e293b"
TEXT_COLOR = "white"
BTN_SUCCESS = "#22c55e"
BTN_SECONDARY = "#475569"

PASSKEYS = {
    "MANAGE AIRLINES": "air123",
    "TICKET COUNTER": "ticket123",
    "ATC": "atc123",
    "CHECKIN": "check123"
}

def create_header(parent, switch_page, back_page, back_args):
    header = tk.Frame(parent, bg=BG_COLOR)
    header.pack(fill="x", pady=10)

    root = parent.winfo_toplevel()
    if back_page:
        root.set_nav_button("Home", lambda: switch_page(back_page, *back_args))

def show_passkey_page(parent, switch_page, module_name, route_callback, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)
    

    card = tk.Frame(parent, bg=CARD_COLOR, width=400, height=250)
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    tk.Label(card,
             text=f"{module_name} LOGIN",
             font=("Segoe UI", 18, "bold"),
             bg=CARD_COLOR,
             fg=TEXT_COLOR).pack(pady=20)

    entry = tk.Entry(card, show="*", font=("Segoe UI", 13), width=25)
    entry.pack(pady=15)
    entry.bind("<Return>", lambda e: verify())

    def verify():
        if entry.get() == PASSKEYS[module_name]:
            route_callback(module_name)
        else:
            messagebox.showerror("Access Denied", "Incorrect Passkey")

    tk.Button(card,
              text="Login",
              bg=BTN_SUCCESS,
              fg="white",
              relief="flat",
              width=15,
              command=verify).pack(pady=10)