import tkinter as tk
from ui.components.card import create_card

def build(parent, callbacks, user):
    frame = tk.Frame(parent, bg="#f2f4f7")

    card = create_card(frame, "Admin Dashboard")
    card.pack(pady=40)

    tk.Label(
        card,
        text=f"Welcome {user['name']}",
        bg="white"
    ).pack(pady=5)

    tk.Button(
        card,
        text="Create User",
        width=25,
        command=callbacks["create_user"]
    ).pack(pady=5)

    tk.Button(
        card,
        text="View Warehouses",
        width=25
    ).pack(pady=5)

    tk.Button(
        card,
        text="System Logs",
        width=25
    ).pack(pady=5)

    tk.Button(
        card,
        text="Logout",
        width=25,
        command=callbacks["logout"]
    ).pack(pady=10)

    return frame