import tkinter as tk


def build(parent, shipments, status_report, callbacks):
    frame = tk.Frame(parent, bg="#f2f4f7")

    title = tk.Label(
        frame,
        text="Shipment Management",
        font=("Arial", 14, "bold"),
        bg="#f2f4f7"
    )
    title.pack(pady=10)

    stats = tk.Frame(frame, bg="#f2f4f7")
    stats.pack(pady=5)

    for idx, key in enumerate(["pending", "in_transit", "delivered", "delayed", "returned"]):
        tk.Label(
            stats,
            text=f"{key.replace('_', ' ').title()}: {status_report.get(key, 0)}",
            bg="#f2f4f7"
        ).grid(row=0, column=idx, padx=8)

    list_frame = tk.Frame(frame, bg="#f2f4f7")
    list_frame.pack(fill="both", expand=True, padx=10, pady=10)

    listbox = tk.Listbox(list_frame, height=14, width=120)
    listbox.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    listbox.config(yscrollcommand=scrollbar.set)

    shipment_ids = []
    for s in shipments:
        shipment_ids.append(s["id"])
        listbox.insert(
            tk.END,
            f"#{s['id']} | {s['shipment_code']} | {s.get('status')} | {s.get('warehouse_name')}")

    def selected_id():
        selected = listbox.curselection()
        if not selected:
            callbacks.get("message", lambda m: None)("Select a shipment")
            return None
        return shipment_ids[selected[0]]

    btns = tk.Frame(frame, bg="#f2f4f7")
    btns.pack(pady=10)

    tk.Button(btns, text="Refresh", width=18, command=callbacks["refresh"]).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(btns, text="Create Shipment", width=18, command=callbacks["create"]).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(btns, text="Assign Driver", width=18, command=lambda: callbacks["assign_driver"](selected_id())).grid(row=0, column=2, padx=5, pady=5)
    tk.Button(btns, text="Update Status", width=18, command=lambda: callbacks["update_status"](selected_id())).grid(row=0, column=3, padx=5, pady=5)
    tk.Button(btns, text="Update Delivery", width=18, command=lambda: callbacks["update_delivery"](selected_id())).grid(row=1, column=0, padx=5, pady=5)
    tk.Button(btns, text="Update Payment", width=18, command=lambda: callbacks["update_payment"](selected_id())).grid(row=1, column=1, padx=5, pady=5)
    tk.Button(btns, text="Report Incident", width=18, command=lambda: callbacks["report_incident"](selected_id())).grid(row=1, column=2, padx=5, pady=5)
    tk.Button(btns, text="View Incidents", width=18, command=lambda: callbacks["view_incidents"](selected_id())).grid(row=1, column=3, padx=5, pady=5)

    tk.Button(frame, text="Back", width=18, command=callbacks["back"]).pack(pady=5)

    return frame
