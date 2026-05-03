import tkinter as tk
from ui.components.card import create_card


def build(parent, on_submit, on_back):
    frame = tk.Frame(parent, bg="#f2f4f7")

    card = create_card(frame, "Create User")
    card.pack(pady=40)

    tk.Label(card, text="Email", bg="white").pack()
    email = tk.Entry(card, width=35)
    email.pack(pady=5)

    tk.Label(card, text="Name", bg="white").pack()
    name = tk.Entry(card, width=35)
    name.pack(pady=5)

    tk.Label(card, text="Password", bg="white").pack()
    password = tk.Entry(card, width=35, show="*")
    password.pack(pady=5)

    tk.Label(card, text="Role", bg="white").pack()
    role = tk.StringVar(value="warehouse_staff")

    tk.OptionMenu(
        card,
        role,
        "manager",
        "driver",
        "warehouse_staff"
    ).pack(pady=5)

    tk.Button(
        card,
        text="Create",
        width=20,
        command=lambda: on_submit(
            email.get(),
            name.get(),
            password.get(),
            role.get()
        )
    ).pack(pady=10)

    tk.Button(
        card,
        text="Back",
        width=20,
        command=on_back
    ).pack()

    return frame