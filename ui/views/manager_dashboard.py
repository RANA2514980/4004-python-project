import tkinter as tk
from ui.components.card import create_card


def build(parent, callbacks, user, service):
    frame = tk.Frame(parent, bg="#f2f4f7")

    # =================================================
    # HEADER
    # =================================================
    header = create_card(frame, "Manager Dashboard")
    header.pack(pady=20)

    tk.Label(
        header,
        text=f"Welcome {user['name']}",
        bg="white",
        font=("Arial", 12, "bold")
    ).pack(pady=5)

    # =================================================
    # KPI SECTION
    # =================================================
    kpi = tk.Frame(frame, bg="#f2f4f7")
    kpi.pack(pady=10)

    total_products = service.get_total_products()
    low_stock_count = len(service.get_low_stock_items())

    tk.Label(
        kpi,
        text=f"Total Products: {total_products}",
        font=("Arial", 11, "bold"),
        bg="#f2f4f7"
    ).grid(row=0, column=0, padx=20)

    tk.Label(
        kpi,
        text=f"Low Stock Items: {low_stock_count}",
        font=("Arial", 11, "bold"),
        bg="#f2f4f7"
    ).grid(row=0, column=1, padx=20)

    # =================================================
    # WAREHOUSE SECTION
    # =================================================
    tk.Label(
        frame,
        text="Warehouses:",
        font=("Arial", 11, "bold"),
        bg="#f2f4f7"
    ).pack(pady=(15, 5))

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

    # =================================================
    # LOW STOCK SECTION
    # =================================================
    tk.Label(
        frame,
        text="Low Stock Alerts",
        font=("Arial", 11, "bold"),
        bg="#f2f4f7"
    ).pack(pady=(15, 5))

    alert_box = tk.Frame(frame, bg="white")
    alert_box.pack(pady=5)

    low_items = service.get_low_stock_items()

    if not low_items:
        tk.Label(
            alert_box,
            text="No low stock items",
            bg="white"
        ).pack()
    else:
        for item in low_items:

            warehouse_data = {
                "id": item["warehouse_id"],
                "name": item.get("warehouse_name", "Unknown")
            }

            tk.Button(
                alert_box,
                # text=f"{item['name']} | Qty: {item['quantity']} | {warehouse_data['name']}",
                text = f"{item['name']} | Qty: {item['quantity']} | Warehouse: {item.get('warehouse_name', 'Unknown')}",
                anchor="w",
                width=60,
                command=lambda ww=warehouse_data:
                    callbacks["open_warehouse"](ww)
            ).pack(fill="x", padx=5, pady=2)

    # =================================================
    # OPERATIONS
    # =================================================
    ops = tk.Frame(frame, bg="#f2f4f7")
    ops.pack(pady=15)

    tk.Button(
        ops,
        text="Manage Vehicles",
        width=20,
        command=callbacks["manage_vehicles"]
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        ops,
        text="Manage Shipments",
        width=20,
        command=callbacks["manage_shipments"]
    ).grid(row=0, column=1, padx=5)

    # =================================================
    # LOGOUT
    # =================================================
    tk.Button(
        frame,
        text="Logout",
        command=callbacks["logout"]
    ).pack(pady=15)

    return frame