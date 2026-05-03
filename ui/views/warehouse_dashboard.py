import tkinter as tk
from ui.components.card import create_card

def build(parent, callbacks, user):
    frame = tk.Frame(parent, bg="#f2f4f7")

    card = create_card(frame, "Warehouse Dashboard")
    card.pack(pady=40)

    tk.Label(card, text=f"Warehouse Staff: {user['name']}", bg="white").pack()

    tk.Button(
        card,
        text="Inventory",
        width=25
    ).pack(pady=5)

    tk.Button(
        card,
        text="Create Shipment",
        width=25,
        command=callbacks["create_shipment"]
    ).pack(pady=5)

    tk.Button(
        card,
        text="Stock Update",
        width=25
    ).pack(pady=5)

    tk.Button(
        card,
        text="Logout",
        width=25,
        command=callbacks["logout"]
    ).pack(pady=10)

    return frame