import tkinter as tk
from tkinter import messagebox

# ===================== MAIN WINDOW =====================
root = tk.Tk()
root.title("Airport Management System")
root.geometry("1000x600")
root.configure(bg="#0f172a")
root.resizable(False, False)

main_container = tk.Frame(root, bg="#0f172a")
main_container.pack(fill="both", expand=True)

current_frame = None

# ===================== PASSKEYS =====================
PASSKEYS = {
    "MANAGE AIRLINES": "air123",
    "TICKET COUNTER": "ticket123",
    "ATC": "atc123",
    "CHECKIN": "check123"
}

# ===================== PAGE SWITCH =====================
def switch_page(page_function, module_name=None):
    global current_frame
    if current_frame is not None:
        current_frame.destroy()

    current_frame = tk.Frame(main_container, bg="#0f172a")
    current_frame.pack(fill="both", expand=True)

    if module_name:
        page_function(current_frame, module_name)
    else:
        page_function(current_frame)

# ===================== HEADER BAR =====================
def create_header(parent, show_logout=False, show_back=False):
    header = tk.Frame(parent, bg="#0f172a")
    header.pack(fill="x", pady=10)

    if show_logout:
        tk.Button(header,
                  text="Logout",
                  bg="#ef4444",
                  fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat",
                  command=lambda: switch_page(show_home)
                  ).pack(side="left", padx=20)

    if show_back:
        tk.Button(header,
                  text="Back",
                  bg="#475569",
                  fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat",
                  command=lambda: switch_page(show_home)
                  ).pack(side="right", padx=20)

# ===================== LOGIN BOX COMPONENT =====================
def create_login_box(parent, module_name):

    card = tk.Frame(parent, bg="#1e293b", width=400, height=250)
    card.place(relx=0.5, rely=0.5, anchor="center")

    card.pack_propagate(False)

    tk.Label(card,
             text=f"{module_name}",
             font=("Segoe UI", 18, "bold"),
             bg="#1e293b",
             fg="white").pack(pady=20)

    tk.Label(card,
             text="Enter Passkey",
             font=("Segoe UI", 12),
             bg="#1e293b",
             fg="#cbd5e1").pack(pady=5)

    entry = tk.Entry(card,
                     show="*",
                     font=("Segoe UI", 13),
                     width=25,
                     relief="flat")
    entry.pack(pady=10)

    def verify():
        if entry.get() == PASSKEYS[module_name]:
            switch_page(show_module_dashboard, module_name)
        else:
            messagebox.showerror("Access Denied", "Incorrect Passkey")

    tk.Button(card,
              text="Login",
              font=("Segoe UI", 12, "bold"),
              bg="#22c55e",
              fg="white",
              relief="flat",
              width=15,
              command=verify).pack(pady=15)

# ===================== HOME PAGE =====================
def show_home(parent):

    tk.Label(parent,
             text="✈ AIRPORT MANAGEMENT SYSTEM",
             font=("Segoe UI", 26, "bold"),
             fg="white",
             bg="#0f172a").pack(pady=60)

    button_frame = tk.Frame(parent, bg="#0f172a")
    button_frame.pack()

    def create_option(text, color):
        return tk.Button(button_frame,
                         text=text,
                         font=("Segoe UI", 14, "bold"),
                         width=25,
                         height=2,
                         bg=color,
                         fg="white",
                         activebackground="#1e293b",
                         relief="flat",
                         command=lambda: switch_page(show_login_page, text))

    create_option("MANAGE AIRLINES", "#2563eb").pack(pady=15)
    create_option("TICKET COUNTER", "#16a34a").pack(pady=15)
    create_option("ATC", "#d97706").pack(pady=15)
    create_option("CHECKIN", "#db2777").pack(pady=15)

# ===================== LOGIN PAGE =====================
def show_login_page(parent, module_name):

    create_header(parent, show_back=True)

    create_login_box(parent, module_name)

# ===================== MODULE DASHBOARD =====================
def show_module_dashboard(parent, module_name):

    create_header(parent, show_logout=True)

    tk.Label(parent,
             text=f"{module_name} DASHBOARD",
             font=("Segoe UI", 24, "bold"),
             fg="white",
             bg="#0f172a").pack(pady=80)

    tk.Label(parent,
             text="Module controls will be implemented here",
             font=("Segoe UI", 14),
             fg="#cbd5e1",
             bg="#0f172a").pack()

# ===================== START =====================
switch_page(show_home)
root.mainloop()