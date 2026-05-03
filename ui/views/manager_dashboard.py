import tkinter as tk
from ui.components.card import create_card

def build(parent, callbacks, user):
    frame = tk.Frame(parent, bg="#f2f4f7")

    card = create_card(frame, "Manager Dashboard")
    card.pack(pady=40)

    tk.Label(card, text=f"Welcome {user['name']}", bg="white").pack()

    tk.Button(card, text="View Shipments", width=25).pack(pady=5)

    tk.Button(
        card,
        text="Assign Driver",
        width=25,
        command=callbacks["assign_driver"]
    ).pack(pady=5)

    tk.Button(card, text="Reports", width=25).pack(pady=5)

    tk.Button(
        card,
        text="Logout",
        width=25,
        command=callbacks["logout"]
    ).pack(pady=10)

    return frame