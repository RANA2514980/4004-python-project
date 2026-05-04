import logging
import tkinter as tk

from ui.views import (
    login_view,
    admin_dashboard,
    manager_dashboard,
    warehouse_dashboard,
    driver_dashboard,
    create_user_view,
    warehouse_detail_view,
    shipment_management_view,
    vehicle_management_view,
    driver_shipments_view
)

from services.auth_service import AuthService
from services.warehouse_assignment_service import WarehouseAssignmentService
from services.manager_service import ManagerService
from services.inventory_service import InventoryService
from services.warehouse_service import WarehouseService
from services.shipment_service import ShipmentService
from services.vehicle_service import VehicleService
from services.audit_service import AuditService

logger = logging.getLogger(__name__)


class TkinterUIAdapter:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Northshore Logistics")
        self.root.geometry("1920x1080")
        self.root.minsize(900, 600)
        self.root.configure(bg="#f2f4f7")

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # STATE
        self.current_user = None
        self._status_var = tk.StringVar(value="")

        # SERVICES
        self.auth_service = AuthService()
        self.audit_service = AuditService(self.auth_service)
        self.warehouse_service = WarehouseService(self.auth_service, self.audit_service)
        self.warehouse_assignment_service = WarehouseAssignmentService(self.auth_service)
        self.manager_service = ManagerService()
        self.inventory_service = InventoryService(self.auth_service, self.audit_service)
        self.shipment_service = ShipmentService(self.auth_service, self.audit_service)
        self.vehicle_service = VehicleService(self.auth_service, self.audit_service)
        
        # LAYOUT
        self.content = tk.Frame(self.root, bg="#f2f4f7")
        self.content.pack(fill=tk.BOTH, expand=True)

        self.footer = tk.Frame(self.root, bg="#e6e9ef", height=30)
        self.footer.pack(fill=tk.X)

        self.status_label = tk.Label(
            self.footer,
            textvariable=self._status_var,
            bg="#e6e9ef",
            fg="#5a6779"
        )
        self.status_label.pack(side=tk.LEFT, padx=10)

        self._show_login()

    # ---------------- CORE ----------------

    def _on_close(self):
        self.root.quit()

    def run(self):
        self.root.mainloop()

    def _clear(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _render(self, builder):
        self._clear()
        frame = builder(self.content)
        frame.pack(fill=tk.BOTH, expand=True)

    # ---------------- LOGIN ----------------

    def _show_login(self):
        self._render(lambda p: login_view.build(p, self._submit_login))

    def _submit_login(self, email, password):
        user = self.auth_service.login(email, password)

        if user:
            self.current_user = user
            self.show_success("Login successful")
            self.show_dashboard(user)
        else:
            self.show_error("Invalid credentials")

    # ---------------- DASHBOARD ----------------

    def show_dashboard(self, user):
        self.current_user = user
        role = user["role"]

        warehouses = self.warehouse_service.list_warehouses()

        callbacks = {
            "create_user": self._show_create_user,
            "create_warehouse": self._show_create_warehouse,
            "open_warehouse": self.open_warehouse_detail,
            "manage_vehicles": self._show_vehicle_management,
            "manage_shipments": self._show_shipment_management,
            "create_shipment": self._show_create_shipment,
            "update_delivery": self._show_update_delivery_status,
            "report_incident": self._show_report_incident,
            "my_shipments": self._show_driver_shipments,
            "inventory": self._open_assigned_warehouse,
            "stock_update": self._open_assigned_warehouse,
            "logout": self._show_login
        }

        if role == "admin":
            self._render(lambda p: admin_dashboard.build(
                p, callbacks, user, warehouses
            ))

        elif role == "manager":
            self._render(lambda p: manager_dashboard.build(
                p,
                callbacks,
                user,
                self.manager_service
            ))
        elif role == "warehouse_staff":
            self._render(lambda p: warehouse_dashboard.build(p, callbacks, user))

        elif role == "driver":
            self._render(lambda p: driver_dashboard.build(p, callbacks, user))

    # ---------------- WAREHOUSE ----------------

    def _show_create_warehouse(self):
        def build(parent):
            frame = tk.Frame(parent, bg="#f2f4f7")

            tk.Label(
                frame,
                text="Create Warehouse",
                font=("Arial", 14, "bold"),
                bg="#f2f4f7"
            ).pack(pady=10)

            name_entry = tk.Entry(frame, width=30)
            name_entry.pack(pady=10)

            def submit():
                success = self.warehouse_service.create_warehouse(
                    name_entry.get().strip(),
                    "Default Location"
                )

                if success:
                    self.show_success("Warehouse created")
                    self.show_dashboard(self.current_user)
                else:
                    self.show_error("Failed to create warehouse")

            tk.Button(frame, text="Create", command=submit).pack(pady=10)

            tk.Button(
                frame,
                text="Back",
                command=lambda: self.show_dashboard(self.current_user)
            ).pack()

            return frame

        self._render(build)

    def open_warehouse_detail(self, warehouse):
        def build(parent):
            return warehouse_detail_view.build(
                parent=parent,
                warehouse=warehouse,
                assignment_service=self.warehouse_assignment_service,
                inventory_service=self.inventory_service,
                on_back=lambda: self.show_dashboard(self.current_user)
            )

        self._render(build)

    # ---------------- USER ----------------

    def _show_create_user(self):
        self._render(lambda p: create_user_view.build(
            p,
            self._submit_create_user,
            lambda: self.show_dashboard(self.current_user)
        ))

    def _submit_create_user(self, email, name, password, role):
        user = self.auth_service.register_user(email, name, password, role)

        if user:
            self.show_success("User created")
            self.show_dashboard(self.current_user)
        else:
            self.show_error("Failed to create user")

    # ---------------- STATUS ----------------

    def _set_status(self, text, style="info"):
        self._status_var.set(text)

        color = {
            "error": "#b42318",
            "success": "#067647",
            "info": "#5a6779"
        }.get(style, "#5a6779")

        self.status_label.config(fg=color)

    def show_error(self, msg):
        self._set_status(msg, "error")

    def show_success(self, msg):
        self._set_status(msg, "success")

    def show_message(self, msg):
        self._set_status(msg, "info")
    
    def _show_vehicle_management(self):
        vehicles = self.vehicle_service.list_all()

        callbacks = {
            "refresh": self._show_vehicle_management,
            "create": self._show_create_vehicle,
            "update_status": self._show_update_vehicle_status,
            "assign_driver": self._show_assign_vehicle_driver,
            "update_maintenance": self._show_update_vehicle_maintenance,
            "message": self.show_message,
            "back": lambda: self.show_dashboard(self.current_user)
        }

        self._render(lambda p: vehicle_management_view.build(p, vehicles, callbacks))

    def _show_shipment_management(self):
        shipments = self.shipment_service.list_all()
        status_report = self.shipment_service.get_status_report()

        callbacks = {
            "refresh": self._show_shipment_management,
            "create": self._show_create_shipment,
            "assign_driver": self._show_assign_driver,
            "update_status": self._show_update_shipment_status,
            "update_delivery": self._show_update_delivery_info,
            "update_payment": self._show_update_payment,
            "report_incident": self._show_report_incident,
            "view_incidents": self._show_view_incidents,
            "message": self.show_message,
            "back": lambda: self.show_dashboard(self.current_user)
        }

        self._render(lambda p: shipment_management_view.build(
            p,
            shipments,
            status_report,
            callbacks
        ))

    # ---------------- SHIPMENTS ----------------

    def _show_create_shipment(self):
        popup = tk.Toplevel(self.root)
        popup.title("Create Shipment")

        fields = {
            "Shipment Code": tk.Entry(popup, width=35),
            "Order Number": tk.Entry(popup, width=35),
            "Sender Name": tk.Entry(popup, width=35),
            "Receiver Name": tk.Entry(popup, width=35),
            "Receiver Address": tk.Entry(popup, width=35),
            "Receiver Phone": tk.Entry(popup, width=35),
            "Description": tk.Entry(popup, width=35),
            "Warehouse ID": tk.Entry(popup, width=35)
        }

        for label, entry in fields.items():
            tk.Label(popup, text=label).pack()
            entry.pack(pady=2)

        def submit():
            try:
                warehouse_id = int(fields["Warehouse ID"].get().strip())
            except ValueError:
                self.show_error("Invalid warehouse ID")
                return

            ok = self.shipment_service.create(
                fields["Shipment Code"].get().strip(),
                fields["Order Number"].get().strip(),
                fields["Sender Name"].get().strip(),
                fields["Receiver Name"].get().strip(),
                fields["Receiver Address"].get().strip(),
                fields["Receiver Phone"].get().strip(),
                fields["Description"].get().strip(),
                warehouse_id
            )
            if ok:
                popup.destroy()
                self.show_success("Shipment created")
                self._show_shipment_management()
            else:
                self.show_error("Create shipment failed")

        tk.Button(popup, text="Create", command=submit).pack(pady=10)

    def _show_assign_driver(self, shipment_id):
        if not shipment_id:
            return

        popup = tk.Toplevel(self.root)
        popup.title("Assign Driver")

        tk.Label(popup, text="Driver ID").pack()
        driver_entry = tk.Entry(popup, width=30)
        driver_entry.pack(pady=5)

        def submit():
            try:
                driver_id = int(driver_entry.get().strip())
            except ValueError:
                self.show_error("Invalid driver ID")
                return

            ok = self.shipment_service.assign_driver(shipment_id, driver_id)
            if ok:
                popup.destroy()
                self.show_success("Driver assigned")
                self._show_shipment_management()
            else:
                self.show_error("Assign failed")

        tk.Button(popup, text="Assign", command=submit).pack(pady=10)

    def _show_update_shipment_status(self, shipment_id):
        if not shipment_id:
            return

        popup = tk.Toplevel(self.root)
        popup.title("Update Status")

        tk.Label(popup, text="Status").pack()
        status = tk.StringVar(value="in_transit")
        tk.OptionMenu(
            popup,
            status,
            "pending",
            "in_transit",
            "delivered",
            "delayed",
            "returned"
        ).pack(pady=5)

        def submit():
            ok = self.shipment_service.update_status(shipment_id, status.get())
            if ok:
                popup.destroy()
                self.show_success("Status updated")
                self._show_shipment_management()
            else:
                self.show_error("Status update failed")

        tk.Button(popup, text="Update", command=submit).pack(pady=10)

    def _show_update_delivery_info(self, shipment_id):
        if not shipment_id:
            return

        popup = tk.Toplevel(self.root)
        popup.title("Update Delivery Info")

        tk.Label(popup, text="Delivery Date (YYYY-MM-DD)").pack()
        delivery_date = tk.Entry(popup, width=30)
        delivery_date.pack(pady=5)

        tk.Label(popup, text="Route Details").pack()
        route_details = tk.Entry(popup, width=30)
        route_details.pack(pady=5)

        def submit():
            ok = self.shipment_service.update_delivery_info(
                shipment_id,
                delivery_date.get().strip(),
                route_details.get().strip()
            )
            if ok:
                popup.destroy()
                self.show_success("Delivery info updated")
                self._show_shipment_management()
            else:
                self.show_error("Delivery update failed")

        tk.Button(popup, text="Update", command=submit).pack(pady=10)

    def _show_update_payment(self, shipment_id):
        if not shipment_id:
            return

        popup = tk.Toplevel(self.root)
        popup.title("Update Payment")

        tk.Label(popup, text="Transport Cost").pack()
        cost_entry = tk.Entry(popup, width=30)
        cost_entry.pack(pady=5)

        tk.Label(popup, text="Payment Status").pack()
        status = tk.StringVar(value="unpaid")
        tk.OptionMenu(popup, status, "paid", "unpaid").pack(pady=5)

        tk.Label(popup, text="Payment Reference").pack()
        reference_entry = tk.Entry(popup, width=30)
        reference_entry.pack(pady=5)

        def submit():
            try:
                cost = float(cost_entry.get().strip())
            except ValueError:
                self.show_error("Invalid cost")
                return

            ok = self.shipment_service.update_financials(
                shipment_id,
                cost,
                status.get(),
                reference_entry.get().strip()
            )
            if ok:
                popup.destroy()
                self.show_success("Payment updated")
                self._show_shipment_management()
            else:
                self.show_error("Payment update failed")

        tk.Button(popup, text="Update", command=submit).pack(pady=10)

    def _show_report_incident(self, shipment_id=None):
        popup = tk.Toplevel(self.root)
        popup.title("Report Incident")

        tk.Label(popup, text="Shipment ID").pack()
        shipment_entry = tk.Entry(popup, width=30)
        shipment_entry.pack(pady=5)

        if shipment_id:
            shipment_entry.insert(0, str(shipment_id))

        tk.Label(popup, text="Incident Type").pack()
        incident_type = tk.StringVar(value="delay")
        tk.OptionMenu(
            popup,
            incident_type,
            "delay",
            "damage",
            "lost",
            "route_change",
            "failed_attempt",
            "other"
        ).pack(pady=5)

        tk.Label(popup, text="Description").pack()
        description = tk.Entry(popup, width=40)
        description.pack(pady=5)

        def submit():
            try:
                sid = int(shipment_entry.get().strip())
            except ValueError:
                self.show_error("Invalid shipment ID")
                return

            ok = self.shipment_service.report_incident(
                sid,
                incident_type.get(),
                description.get().strip()
            )
            if ok:
                popup.destroy()
                self.show_success("Incident reported")
                if self.current_user and self.current_user.get("role") == "driver":
                    self._show_driver_shipments()
                else:
                    self._show_shipment_management()
            else:
                self.show_error("Incident report failed")

        tk.Button(popup, text="Report", command=submit).pack(pady=10)

    def _show_view_incidents(self, shipment_id):
        if not shipment_id:
            return

        incidents = self.shipment_service.list_incidents(shipment_id)

        popup = tk.Toplevel(self.root)
        popup.title("Shipment Incidents")

        if not incidents:
            tk.Label(popup, text="No incidents").pack(pady=10)
            return

        listbox = tk.Listbox(popup, width=90, height=12)
        listbox.pack(padx=10, pady=10)

        for inc in incidents:
            listbox.insert(
                tk.END,
                f"#{inc['id']} | {inc['incident_type']} | {inc['status']} | {inc.get('reported_at')}")

    def _show_update_delivery_status(self):
        self._show_driver_shipments()

    def _show_driver_shipments(self):
        if not self.current_user:
            return

        shipments = self.shipment_service.driver_shipments(self.current_user["id"])
        callbacks = {
            "refresh": self._show_driver_shipments,
            "update_status": self._show_update_shipment_status,
            "report_incident": self._show_report_incident,
            "message": self.show_message,
            "back": lambda: self.show_dashboard(self.current_user)
        }

        self._render(lambda p: driver_shipments_view.build(p, shipments, callbacks))

    # ---------------- VEHICLES ----------------

    def _show_create_vehicle(self):
        popup = tk.Toplevel(self.root)
        popup.title("Create Vehicle")

        tk.Label(popup, text="Vehicle Code").pack()
        code = tk.Entry(popup, width=30)
        code.pack(pady=5)

        tk.Label(popup, text="Capacity").pack()
        capacity = tk.Entry(popup, width=30)
        capacity.pack(pady=5)

        def submit():
            try:
                cap = int(capacity.get().strip())
            except ValueError:
                self.show_error("Invalid capacity")
                return

            ok = self.vehicle_service.create(code.get().strip(), cap)
            if ok:
                popup.destroy()
                self.show_success("Vehicle created")
                self._show_vehicle_management()
            else:
                self.show_error("Vehicle create failed")

        tk.Button(popup, text="Create", command=submit).pack(pady=10)

    def _show_update_vehicle_status(self, vehicle_id):
        if not vehicle_id:
            return

        popup = tk.Toplevel(self.root)
        popup.title("Update Vehicle Status")

        tk.Label(popup, text="Status").pack()
        status = tk.StringVar(value="available")
        tk.OptionMenu(popup, status, "available", "in_use", "maintenance").pack(pady=5)

        def submit():
            ok = self.vehicle_service.update(vehicle_id, status=status.get())
            if ok:
                popup.destroy()
                self.show_success("Vehicle updated")
                self._show_vehicle_management()
            else:
                self.show_error("Vehicle update failed")

        tk.Button(popup, text="Update", command=submit).pack(pady=10)

    def _show_assign_vehicle_driver(self, vehicle_id):
        if not vehicle_id:
            return

        popup = tk.Toplevel(self.root)
        popup.title("Assign Driver")

        tk.Label(popup, text="Driver ID").pack()
        driver_id = tk.Entry(popup, width=30)
        driver_id.pack(pady=5)

        def submit():
            try:
                assigned_id = int(driver_id.get().strip())
            except ValueError:
                self.show_error("Invalid driver ID")
                return

            ok = self.vehicle_service.update(vehicle_id, assigned_driver_id=assigned_id)
            if ok:
                popup.destroy()
                self.show_success("Driver assigned")
                self._show_vehicle_management()
            else:
                self.show_error("Assign failed")

        tk.Button(popup, text="Assign", command=submit).pack(pady=10)

    def _show_update_vehicle_maintenance(self, vehicle_id):
        if not vehicle_id:
            return

        popup = tk.Toplevel(self.root)
        popup.title("Update Maintenance Dates")

        tk.Label(popup, text="Last Service Date (YYYY-MM-DD)").pack()
        last_service = tk.Entry(popup, width=30)
        last_service.pack(pady=5)

        tk.Label(popup, text="Maintenance Due Date (YYYY-MM-DD)").pack()
        due_date = tk.Entry(popup, width=30)
        due_date.pack(pady=5)

        def submit():
            ok = self.vehicle_service.update(
                vehicle_id,
                last_service_date=last_service.get().strip(),
                maintenance_due_date=due_date.get().strip()
            )
            if ok:
                popup.destroy()
                self.show_success("Maintenance updated")
                self._show_vehicle_management()
            else:
                self.show_error("Maintenance update failed")

        tk.Button(popup, text="Update", command=submit).pack(pady=10)

    def _open_assigned_warehouse(self):
        if not self.current_user:
            return

        assignment = self.warehouse_assignment_service.get_assignment_for_user(
            self.current_user["id"]
        )
        if not assignment:
            self.show_error("No warehouse assignment")
            return

        self.open_warehouse_detail(assignment)