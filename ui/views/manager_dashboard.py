import tkinter as tk
from ui.components.card import create_card


def build(parent, callbacks, user, service):
    frame = tk.Frame(parent, bg="#f2f4f7")

    # ---------------- HEADER ----------------
    header = create_card(frame, "Manager Dashboard")
    header.pack(pady=20)

    tk.Label(
        header,
        text=f"Welcome {user['name']}",
        bg="white",
        font=("Arial", 12, "bold")
    ).pack(pady=5)

    # ---------------- KPI SECTION ----------------
    kpi = tk.Frame(frame, bg="#f2f4f7")
    kpi.pack(pady=10)

    total_products = service.get_total_products()
    low_stock = len(service.get_low_stock_items())

    tk.Label(kpi, text=f"Total Products: {total_products}").pack()
    tk.Label(kpi, text=f"Low Stock Items: {low_stock}").pack()

    # ---------------- WAREHOUSES ----------------
    tk.Label(frame, text="Warehouses:", font=("Arial", 11, "bold"),
             bg="#f2f4f7").pack(pady=10)

    warehouse_container = tk.Frame(frame, bg="#f2f4f7")
    warehouse_container.pack()

    warehouses = service.get_all_warehouses()

    cols = 3
    r = 0
    c = 0

    for w in warehouses:
        tk.Button(
            warehouse_container,
            text=w["name"],
            width=22,
            command=lambda ww=w: callbacks["open_warehouse"](ww)
        ).grid(row=r, column=c, padx=5, pady=5)

        c += 1
        if c >= cols:
            c = 0
            r += 1

    # ---------------- LOW STOCK ----------------
    tk.Label(frame, text="Low Stock Alerts",
             font=("Arial", 11, "bold"),
             bg="#f2f4f7").pack(pady=10)

    alert_box = tk.Frame(frame, bg="white")
    alert_box.pack(pady=5)

    low_items = service.get_low_stock_items()

    if not low_items:
        tk.Label(alert_box, text="No low stock items", bg="white").pack()
    else:
        for item in low_items:
            tk.Label(
                alert_box,
                text=f"{item['name']} ({item['quantity']})",
                bg="white"
            ).pack(anchor="w")

    # ---------------- LOGOUT ----------------
    tk.Button(
        frame,
        text="Logout",
        command=callbacks["logout"]
    ).pack(pady=15)

    return frame