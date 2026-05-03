import tkinter as tk


def build(parent, warehouse, service, on_back):
    frame = tk.Frame(parent, bg="#f2f4f7")

    # ---------------- HEADER ----------------
    tk.Label(
        frame,
        text=f"Warehouse: {warehouse['name']}",
        font=("Arial", 14, "bold"),
        bg="#f2f4f7"
    ).pack(pady=10)

    # ---------------- MAIN LAYOUT ----------------
    container = tk.Frame(frame, bg="#f2f4f7")
    container.pack(fill="both", expand=True)

    left_panel = tk.Frame(container, bg="white", width=300)
    left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    right_panel = tk.Frame(container, bg="white", width=300)
    right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # ---------------- TITLES ----------------
    tk.Label(left_panel, text="Unassigned Staff", bg="white", font=("Arial", 11, "bold")).pack(pady=5)
    tk.Label(right_panel, text="Assigned Staff", bg="white", font=("Arial", 11, "bold")).pack(pady=5)

    # ---------------- STATE ----------------
    vars_map = {}
    assigned_container = tk.Frame(right_panel, bg="white")
    assigned_container.pack(fill="both", expand=True)

    unassigned_container = tk.Frame(left_panel, bg="white")
    unassigned_container.pack(fill="both", expand=True)

    status = tk.Label(frame, text="", bg="#f2f4f7")
    status.pack()

    # ---------------- LOAD DATA ----------------
    def refresh():
        # clear UI
        for w in unassigned_container.winfo_children():
            w.destroy()
        for w in assigned_container.winfo_children():
            w.destroy()

        vars_map.clear()

        # fetch data
        unassigned = service.get_unassigned_staff()
        assigned = service.get_assigned_staff(warehouse["id"])

        # ---------------- UNASSIGNED ----------------
        for user in unassigned:
            var = tk.BooleanVar()
            vars_map[user["id"]] = var

            tk.Checkbutton(
                unassigned_container,
                text=f"{user['name']} ({user['email']})",
                variable=var,
                bg="white"
            ).pack(anchor="w")

        # ---------------- ASSIGNED ----------------
        if not assigned:
            tk.Label(assigned_container, text="No staff assigned", bg="white").pack()
        else:
            for user in assigned:
                tk.Label(
                    assigned_container,
                    text=f"{user['name']} ({user['email']})",
                    bg="white"
                ).pack(anchor="w")

    # initial load
    refresh()

    # ---------------- ASSIGN ----------------
    def assign():
        user_ids = [uid for uid, var in vars_map.items() if var.get()]

        if not user_ids:
            status.config(text="No staff selected", fg="red")
            return

        ok = service.assign_users(warehouse["id"], user_ids)

        if ok:
            status.config(text="Assigned successfully", fg="green")
            refresh()
        else:
            status.config(text="Assignment failed", fg="red")

    # ---------------- BUTTONS ----------------
    btn_frame = tk.Frame(frame, bg="#f2f4f7")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Assign Selected", command=assign).pack(side="left", padx=5)
    tk.Button(
        btn_frame,
            text="Back",
            command=lambda: on_back()
        ).pack(side="left", padx=5)
    
    
    return frame