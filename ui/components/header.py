import tkinter as tk

def create_card(parent, title=None):
    card = tk.Frame(parent, bg="white", padx=20, pady=20, bd=1, relief="solid")

    if title:
        tk.Label(
            card,
            text=title,
            font=("TkDefaultFont", 12, "bold"),
            bg="white"
        ).pack(pady=(0, 10))

    return card