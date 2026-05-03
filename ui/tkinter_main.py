import logging
import tkinter as tk

from ui.views import (
    login_view,
    admin_dashboard,
    manager_dashboard,
    warehouse_dashboard,
    driver_dashboard,
    create_user_view,
    warehouse_detail_view
)

from services.auth_service import AuthService
from services.warehouse_assignment_service import WarehouseAssignmentService
from repositories.warehouse_repository import WarehouseRepository
from services.manager_service import ManagerService
from services.inventory_service import InventoryService

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
        self.warehouse_repo = WarehouseRepository()
        self.warehouse_assignment_service = WarehouseAssignmentService(self.auth_service)
        self.manager_service = ManagerService()
        self.inventory_service = InventoryService(self.auth_service)
        
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

        warehouses = self.warehouse_repo.list_warehouses()

        callbacks = {
            "create_user": self._show_create_user,
            "create_warehouse": self._show_create_warehouse,
            "open_warehouse": self.open_warehouse_detail,
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
                success = self.warehouse_repo.create_warehouse(
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