# auth_module.py

import tkinter as tk
from tkinter import messagebox

BG_COLOR = "#0b0f19"
CARD_COLOR = "#151f32"
BORDER_COLOR = "#243249"
TEXT_COLOR = "#f8fafc"
SUB_TEXT = "#94a3b8"
BTN_SUCCESS = "#10b981"
SUCCESS_HOVER = "#34d399"

PASSKEYS = {
    "MANAGE AIRLINES": "air123",
    "TICKET COUNTER": "ticket123",
    "ATC": "atc123",
    "CHECKIN": "check123"
}

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

def create_header(parent, switch_page, back_page, back_args):
    root = parent.winfo_toplevel()
    if back_page:
        root.set_nav_button("Home", lambda: switch_page(back_page, *back_args))

def show_passkey_page(parent, switch_page, module_name, route_callback, back_page, back_args):
    parent.configure(bg=BG_COLOR)
    create_header(parent, switch_page, back_page, back_args)
    
    content_wrapper = tk.Frame(parent, bg=BG_COLOR)
    content_wrapper.pack(expand=True, fill="both", pady=40)

    # High fidelity card container
    card = tk.Frame(content_wrapper, bg=CARD_COLOR, bd=1, highlightbackground=BORDER_COLOR, highlightthickness=1, width=420, height=320)
    card.pack(expand=True)
    card.pack_propagate(False)

    # Accent top border line
    accent_bar = tk.Frame(card, bg="#6366f1", height=4)
    accent_bar.pack(fill="x", side="top")

    # Security Lock Icon
    tk.Label(card, text="🔒", font=("Segoe UI", 36), fg="#6366f1", bg=CARD_COLOR).pack(pady=(20, 5))

    tk.Label(card,
             text=f"{module_name} ACCESS",
             font=("Segoe UI", 16, "bold"),
             bg=CARD_COLOR,
             fg=TEXT_COLOR).pack(pady=5)

    tk.Label(card,
             text="Please enter your authorization passkey:",
             font=("Segoe UI", 10),
             bg=CARD_COLOR,
             fg=SUB_TEXT).pack(pady=(0, 15))

    # Styled Entry container
    entry_frame = tk.Frame(card, bg=BORDER_COLOR, padx=1, pady=1)
    entry_frame.pack(pady=5)
    
    entry = tk.Entry(entry_frame, show="*", font=("Segoe UI", 13), width=25, bg="#111827", fg="white", insertbackground="white", relief="flat")
    entry.pack(padx=2, pady=2)
    entry.focus_set()
    
    def verify():
        if entry.get() == PASSKEYS[module_name]:
            route_callback(module_name)
        else:
            messagebox.showerror("Access Denied", "Incorrect Passkey")

    entry.bind("<Return>", lambda e: verify())

    btn = tk.Button(card,
                    text="Authenticate Access",
                    bg=BTN_SUCCESS,
                    fg="white",
                    relief="flat",
                    font=("Segoe UI", 11, "bold"),
                    width=20,
                    height=1,
                    cursor="hand2",
                    activebackground=SUCCESS_HOVER,
                    activeforeground="white",
                    command=verify)
    btn.pack(pady=20)
    add_hover(btn, SUCCESS_HOVER, BTN_SUCCESS)