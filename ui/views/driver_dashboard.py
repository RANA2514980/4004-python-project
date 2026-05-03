import tkinter as tk
from ui.components.card import create_card

def build(parent, callbacks, user):
    frame = tk.Frame(parent, bg="#f2f4f7")

    card = create_card(frame, "Driver Dashboard")
    card.pack(pady=40)

    tk.Label(card, text=f"Driver: {user['name']}", bg="white").pack()

    tk.Button(
        card,
        text="My Shipments",
        width=25
    ).pack(pady=5)

    tk.Button(
        card,
        text="Update Delivery Status",
        width=25,
        command=callbacks["update_delivery"]
    ).pack(pady=5)

    tk.Button(
        card,
        text="Report Incident",
        width=25
    ).pack(pady=5)

    tk.Button(
        card,
        text="Logout",
        width=25,
        command=callbacks["logout"]
    ).pack(pady=10)

    return frame