import tkinter as tk


def build(parent, vehicles, callbacks):
    frame = tk.Frame(parent, bg="#f2f4f7")

    tk.Label(
        frame,
        text="Vehicle Management",
        font=("Arial", 14, "bold"),
        bg="#f2f4f7"
    ).pack(pady=10)

    list_frame = tk.Frame(frame, bg="#f2f4f7")
    list_frame.pack(fill="both", expand=True, padx=10, pady=10)

    listbox = tk.Listbox(list_frame, height=14, width=100)
    listbox.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    listbox.config(yscrollcommand=scrollbar.set)

    vehicle_ids = []
    for v in vehicles:
        vehicle_ids.append(v["id"])
        listbox.insert(
            tk.END,
            f"#{v['id']} | {v['vehicle_code']} | {v.get('status')} | cap={v.get('capacity')}"
        )

    def selected_id():
        selected = listbox.curselection()
        if not selected:
            callbacks.get("message", lambda m: None)("Select a vehicle")
            return None
        return vehicle_ids[selected[0]]

    btns = tk.Frame(frame, bg="#f2f4f7")
    btns.pack(pady=10)

    tk.Button(btns, text="Refresh", width=18, command=callbacks["refresh"]).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(btns, text="Create Vehicle", width=18, command=callbacks["create"]).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(btns, text="Update Status", width=18, command=lambda: callbacks["update_status"](selected_id())).grid(row=0, column=2, padx=5, pady=5)
    tk.Button(btns, text="Assign Driver", width=18, command=lambda: callbacks["assign_driver"](selected_id())).grid(row=1, column=0, padx=5, pady=5)
    tk.Button(btns, text="Maintenance Dates", width=18, command=lambda: callbacks["update_maintenance"](selected_id())).grid(row=1, column=1, padx=5, pady=5)

    tk.Button(frame, text="Back", width=18, command=callbacks["back"]).pack(pady=5)

    return frame
