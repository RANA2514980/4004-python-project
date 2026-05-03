import tkinter as tk
from ui.components.card import create_card


def build(parent, callbacks, user, warehouses):
    frame = tk.Frame(parent, bg="#f2f4f7")

    card = create_card(frame, "Admin Dashboard")
    card.pack(pady=30)

    tk.Label(
        card,
        text=f"Welcome {user['name']}",
        bg="white",
        font=("Arial", 11, "bold")
    ).pack(pady=5)

    # ---------------- ACTION BUTTONS ----------------

    tk.Button(
        card,
        text="Create User",
        width=25,
        command=callbacks["create_user"]
    ).pack(pady=5)

    tk.Button(
        card,
        text="Create Warehouse",
        width=25,
        command=callbacks["create_warehouse"]
    ).pack(pady=5)

    tk.Button(
        card,
        text="Logout",
        width=25,
        command=callbacks["logout"]
    ).pack(pady=10)

    # ---------------- WAREHOUSE LIST ----------------

    tk.Label(
        card,
        text="Warehouses:",
        bg="white",
        font=("Arial", 11, "bold")
    ).pack(pady=(20, 5))

    container = tk.Frame(card, bg="white")
    container.pack()

    if not warehouses:
        tk.Label(container, text="No warehouses yet", bg="white").pack()
        return frame

    cols = 3
    row = 0
    col = 0

    for w in warehouses:
        tk.Button(
            container,
            text=w["name"],
            width=20,
            command=lambda ww=w: callbacks["open_warehouse"](ww)
        ).grid(row=row, column=col, padx=5, pady=5)

        col += 1
        if col >= cols:
            col = 0
            row += 1

    return frame