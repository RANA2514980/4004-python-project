import logging
import tkinter as tk

from ui.views import login_view
from ui.views import admin_dashboard
from ui.views import manager_dashboard
from ui.views import warehouse_dashboard
from ui.views import driver_dashboard
from ui.views import create_user_view

logger = logging.getLogger(__name__)


class TkinterUIAdapter:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Northshore Logistics")
        self.root.geometry("980x640")
        self.root.minsize(900, 600)
        self.root.configure(bg="#f2f4f7")

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # state
        self._closed = False
        self._login_result = (None, None)
        self._status_var = tk.StringVar(value="")
        self.current_user = None

        # layout
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

        # ❌ REMOVE pages system completely (IMPORTANT FIX)
        # self.pages = {}
        # self._build_pages()

        self._show_login()

    # -----------------------------
    # WINDOW CONTROL
    # -----------------------------

    def _on_close(self):
        self._closed = True
        self.root.quit()

    def run(self):
        self.root.mainloop()

    # -----------------------------
    # SCREEN RENDERING (FIXED)
    # -----------------------------

    def _clear_screen(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _render(self, build_fn):
        self._clear_screen()
        frame = build_fn(self.content)
        frame.pack(fill=tk.BOTH, expand=True)

    # -----------------------------
    # LOGIN
    # -----------------------------

    def _show_login(self):
        self._render(lambda parent: login_view.build(parent, self._submit_login))

    def _submit_login(self, email, password):
        from services.auth_service import AuthService

        auth_service = AuthService()

        user = auth_service.login(email, password)

        if user:
            self.show_success("Login successful")
            self.show_dashboard(user)
        else:
            self.show_error("Invalid email or password")

    def get_login_input(self):
        return self._login_result

    # -----------------------------
    # DASHBOARD
    # -----------------------------

    def show_dashboard(self, user, callbacks=None):
        self.current_user = user
        role = user["role"]
        callbacks = callbacks or {
            "create_user": self._show_create_user,
            "manage_warehouses": lambda: self.show_message("Manage Warehouses clicked"),
            "view_reports": lambda: self.show_message("Reports clicked"),
            "logout": self._show_login
        }

        if role == "admin":
            self._render(lambda p: admin_dashboard.build(p, callbacks, user))

        elif role == "manager":
            self._render(lambda p: manager_dashboard.build(p, callbacks, user))

        elif role == "warehouse_staff":
            self._render(lambda p: warehouse_dashboard.build(p, callbacks, user))

        elif role == "driver":
            self._render(lambda p: driver_dashboard.build(p, callbacks, user))

        else:
            self._set_status("Invalid role", "error")
    
    def _show_create_user(self):
        self._render(
            lambda p: create_user_view.build(
                p,
                self._submit_create_user,
                lambda: self.show_dashboard(self.current_user)
            )
        )
    
    
    def _submit_create_user(self, email, name, password, role):
        from services.auth_service import AuthService

        auth = AuthService()
        auth.current_user = self.current_user

        user = auth.register_user(email, name, password, role)

        if user:
            self.show_success("User created successfully")
            self.show_dashboard(self.current_user)
        else:
            self.show_error("Failed to create user")
    
    

    # -----------------------------
    # STATUS BAR
    # -----------------------------

    def _set_status(self, text, style="info"):
        self._status_var.set(text)

        if style == "error":
            self.status_label.config(fg="#b42318")
        elif style == "success":
            self.status_label.config(fg="#067647")
        else:
            self.status_label.config(fg="#5a6779")

    def show_error(self, message):
        self._set_status(message, "error")

    def show_success(self, message):
        self._set_status(message, "success")

    def show_message(self, message):
        self._set_status(message, "info")