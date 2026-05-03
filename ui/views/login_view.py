import tkinter as tk
from ui.components.card import create_card

def build(parent, on_login):
    frame = tk.Frame(parent, bg="#f2f4f7")

    card = create_card(frame, "Login")
    card.pack(pady=80)

    tk.Label(card, text="Email", bg="white").pack(anchor="w")
    email = tk.Entry(card, width=35)
    email.pack(pady=5)

    tk.Label(card, text="Password", bg="white").pack(anchor="w")
    password = tk.Entry(card, width=35, show="*")
    password.pack(pady=5)

    def submit():
        on_login(email.get(), password.get())

    tk.Button(card, text="Login", command=submit).pack(pady=10)

    return frame