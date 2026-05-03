import tkinter as tk
from functools import partial


def build(parent, warehouse, assignment_service, inventory_service, on_back):
    frame = tk.Frame(parent, bg="#f2f4f7")

    tk.Label(
        frame,
        text=f"Warehouse: {warehouse['name']}",
        font=("Arial", 15, "bold"),
        bg="#f2f4f7"
    ).pack(pady=10)

    container = tk.Frame(frame, bg="#f2f4f7")
    container.pack(fill="both", expand=True)

    # =================================================
    # PANELS
    # =================================================

    left = tk.Frame(container, bg="white")
    left.pack(side="left", fill="both", expand=True, padx=8, pady=8)

    middle = tk.Frame(container, bg="white")
    middle.pack(side="left", fill="both", expand=True, padx=8, pady=8)

    right = tk.Frame(container, bg="white")
    right.pack(side="left", fill="both", expand=True, padx=8, pady=8)

    tk.Label(left, text="Unassigned Staff",
             font=("Arial", 11, "bold"), bg="white").pack(pady=5)

    tk.Label(middle, text="Assigned Staff",
             font=("Arial", 11, "bold"), bg="white").pack(pady=5)

    tk.Label(right, text="Inventory",
             font=("Arial", 11, "bold"), bg="white").pack(pady=5)

    unassigned_container = tk.Frame(left, bg="white")
    unassigned_container.pack(fill="both", expand=True)

    assigned_container = tk.Frame(middle, bg="white")
    assigned_container.pack(fill="both", expand=True)

    inventory_container = tk.Frame(right, bg="white")
    inventory_container.pack(fill="both", expand=True)

    vars_map = {}

    status = tk.Label(frame, bg="#f2f4f7")
    status.pack()

    # =================================================
    # REFRESH
    # =================================================

    def refresh():
        for c in [
            unassigned_container,
            assigned_container,
            inventory_container
        ]:
            for w in c.winfo_children():
                w.destroy()

        vars_map.clear()

        # ---------------- UNASSIGNED ----------------
        unassigned = assignment_service.get_unassigned_staff()

        for user in unassigned:
            var = tk.BooleanVar()
            vars_map[user["id"]] = var

            tk.Checkbutton(
                unassigned_container,
                text=user["name"],
                variable=var,
                bg="white"
            ).pack(anchor="w")

        # ---------------- ASSIGNED ----------------
        assigned = assignment_service.get_assigned_staff(
            warehouse["id"]
        )

        if not assigned:
            tk.Label(
                assigned_container,
                text="No assigned staff",
                bg="white"
            ).pack()

        for user in assigned:
            row = tk.Frame(assigned_container, bg="white")
            row.pack(fill="x", pady=2)

            tk.Label(
                row,
                text=user["name"],
                bg="white"
            ).pack(side="left")

            tk.Button(
                row,
                text="Remove",
                command=partial(remove_staff, user["id"])
            ).pack(side="right")

        # ---------------- INVENTORY ----------------
        inventory = inventory_service.list_inventory(
            warehouse["id"]
        )

        if not inventory:
            tk.Label(
                inventory_container,
                text="No inventory",
                bg="white"
            ).pack()

        for item in inventory:
            tk.Label(
                inventory_container,
                text=f"{item['name']} | Qty: {item['quantity']}",
                bg="white"
            ).pack(anchor="w")

    # =================================================
    # STAFF ACTIONS
    # =================================================

    def assign():
        ids = [uid for uid, v in vars_map.items() if v.get()]

        if not ids:
            status.config(text="Select staff", fg="red")
            return

        if assignment_service.assign_users(
            warehouse["id"],
            ids
        ):
            status.config(text="Assigned", fg="green")
            refresh()

    def remove_staff(user_id):
        ok = assignment_service.remove_assignment(user_id)

        if ok:
            status.config(
                text=f"Removed staff {user_id}",
                fg="green"
            )
            refresh()
        else:
            status.config(
                text="Remove failed",
                fg="red"
            )

    # =================================================
    # INVENTORY
    # =================================================

    def add_inventory():
        popup = tk.Toplevel()
        popup.title("Add Inventory")

        tk.Label(popup, text="product code").pack()
        sku = tk.Entry(popup)
        sku.pack()

        tk.Label(popup, text="Name").pack()
        name = tk.Entry(popup)
        name.pack()

        tk.Label(popup, text="Quantity").pack()
        qty = tk.Entry(popup)
        qty.pack()

        def submit():
            ok = inventory_service.add_product_to_warehouse(
                warehouse["id"],
                sku.get(),
                name.get(),
                int(qty.get())
            )

            if ok:
                popup.destroy()
                refresh()

        tk.Button(
            popup,
            text="Add",
            command=submit
        ).pack(pady=10)

    # =================================================
    # BUTTONS
    # =================================================

    btn = tk.Frame(frame, bg="#f2f4f7")
    btn.pack(pady=10)

    tk.Button(btn, text="Assign Staff",
              command=assign).pack(side="left", padx=5)

    tk.Button(btn, text="Add Inventory",
              command=add_inventory).pack(side="left", padx=5)

    tk.Button(btn, text="Back",
              command=on_back).pack(side="left", padx=5)

    refresh()

    return frame