import logging
import tkinter as tk
from ui.adapter import UIAdapter

logger = logging.getLogger(__name__)


class TkinterUIAdapter(UIAdapter):

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Northshore Logistics")
        self.root.geometry("980x640")
        self.root.minsize(900, 600)
        self.root.configure(bg="#f2f4f7")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self.choice_var = tk.StringVar(value="")
        self._closed = False
        self._last_is_admin = False

        self._login_result = (None, None)
        self._password_reset_result = (None, None, None)
        self._create_user_result = (None, None, None, None)
        self._status_var = tk.StringVar(value="")
        self._status_style = "info"
        self._profile_back = tk.BooleanVar(value=False)

        self._build_shell()
        self._build_pages()
        self._show_page("login")

    def _on_close(self):
        self._closed = True
        self.choice_var.set("__exit__")
        self.root.quit()

    def _build_shell(self):
        self.header = tk.Frame(self.root, bg="#1f3b5c", height=60)
        self.header.pack(fill=tk.X)

        self.header_title = tk.Label(
            self.header,
            text="Data Management System",
            font=("TkDefaultFont", 16, "bold"),
            bg="#1f3b5c",
            fg="#f5f7fb"
        )
        self.header_title.pack(side=tk.LEFT, padx=20, pady=12)

        self.nav_frame = tk.Frame(self.header, bg="#1f3b5c")
        self.nav_frame.pack(side=tk.RIGHT, padx=12)

        self.content = tk.Frame(self.root, bg="#f2f4f7")
        self.content.pack(fill=tk.BOTH, expand=True)

        self.footer = tk.Frame(self.root, bg="#e6e9ef", height=32)
        self.footer.pack(fill=tk.X)

        self.status_label = tk.Label(
            self.footer,
            textvariable=self._status_var,
            font=("TkDefaultFont", 9),
            bg="#e6e9ef",
            fg="#5a6779"
        )
        self.status_label.pack(side=tk.LEFT, padx=16)

    def _build_pages(self):
        self.pages = {}

        self.pages["auth_menu"] = self._build_auth_menu()
        self.pages["login"] = self._build_login()
        self.pages["reset_password"] = self._build_reset_password()
        self.pages["create_user"] = self._build_create_user()
        self.pages["profile"] = self._build_profile()

    def _show_page(self, key):
        for page in self.pages.values():
            page.pack_forget()
        self.pages[key].pack(fill=tk.BOTH, expand=True)

    def _set_nav_buttons(self, items):
        for child in self.nav_frame.winfo_children():
            child.destroy()
        for label, value in items:
            tk.Button(
                self.nav_frame,
                text=label,
                width=12,
                command=lambda v=value: self.choice_var.set(v)
            ).pack(side=tk.RIGHT, padx=6, pady=12)

    def _build_auth_menu(self):
        frame = tk.Frame(self.content, bg="#f2f4f7")

        self.auth_title = tk.Label(
            frame,
            text="",
            font=("TkDefaultFont", 12, "bold"),
            bg="#f2f4f7",
            fg="#2a3442"
        )
        self.auth_title.pack(pady=(24, 10))

        self.auth_buttons = tk.Frame(frame, bg="#f2f4f7")
        self.auth_buttons.pack(pady=8)

        return frame

    def _rebuild_auth_menu_buttons(self):
        for child in self.auth_buttons.winfo_children():
            child.destroy()

        if self._last_is_admin:
            tk.Button(
                self.auth_buttons,
                text="Create User",
                width=28,
                command=lambda: self.choice_var.set("3")
            ).pack(pady=4)

            tk.Button(
                self.auth_buttons,
                text="Logout",
                width=28,
                command=lambda: self.choice_var.set("4")
            ).pack(pady=4)
        else:
            tk.Button(
                self.auth_buttons,
                text="Logout",
                width=28,
                command=lambda: self.choice_var.set("3")
            ).pack(pady=4)

    def _build_login(self):
        frame = tk.Frame(self.content, bg="#f2f4f7")

        card = tk.Frame(frame, bg="#ffffff", padx=30, pady=24)
        card.pack(pady=50)

        tk.Label(
            card,
            text="Login",
            font=("TkDefaultFont", 13, "bold"),
            bg="#ffffff",
            fg="#1c2533"
        ).pack(pady=(0, 16))

        tk.Label(card, text="Email", bg="#ffffff").pack(anchor="w")
        self.login_email = tk.Entry(card, width=36)
        self.login_email.pack(pady=(0, 12))

        tk.Label(card, text="Password", bg="#ffffff").pack(anchor="w")
        self.login_password = tk.Entry(card, width=36, show="*")
        self.login_password.pack(pady=(0, 16))

        btn_row = tk.Frame(card, bg="#ffffff")
        btn_row.pack()

        tk.Button(
            btn_row,
            text="Login",
            width=18,
            command=self._submit_login
        ).pack(side=tk.LEFT, padx=6)

        return frame

    def _submit_login(self):
        self._login_result = (
            self.login_email.get().strip(),
            self.login_password.get().strip()
        )
        self.choice_var.set("1")

    def _build_reset_password(self):
        frame = tk.Frame(self.content, bg="#f2f4f7")

        card = tk.Frame(frame, bg="#ffffff", padx=30, pady=24)
        card.pack(pady=50)

        tk.Label(
            card,
            text="Reset Password",
            font=("TkDefaultFont", 13, "bold"),
            bg="#ffffff",
            fg="#1c2533"
        ).pack(pady=(0, 16))

        tk.Label(card, text="Current Password", bg="#ffffff").pack(anchor="w")
        self.current_password = tk.Entry(card, width=36, show="*")
        self.current_password.pack(pady=(0, 12))

        tk.Label(card, text="New Password", bg="#ffffff").pack(anchor="w")
        self.new_password = tk.Entry(card, width=36, show="*")
        self.new_password.pack(pady=(0, 12))

        tk.Label(card, text="Confirm Password", bg="#ffffff").pack(anchor="w")
        self.confirm_password = tk.Entry(card, width=36, show="*")
        self.confirm_password.pack(pady=(0, 16))

        btn_row = tk.Frame(card, bg="#ffffff")
        btn_row.pack()

        tk.Button(
            btn_row,
            text="Update",
            width=14,
            command=self._submit_password_reset
        ).pack(side=tk.LEFT, padx=6)

        tk.Button(
            btn_row,
            text="Back",
            width=14,
            command=self._cancel_password_reset
        ).pack(side=tk.LEFT, padx=6)

        return frame

    def _submit_password_reset(self):
        self._password_reset_result = (
            self.current_password.get().strip(),
            self.new_password.get().strip(),
            self.confirm_password.get().strip()
        )
        self.choice_var.set("__reset__")

    def _cancel_password_reset(self):
        self._password_reset_result = (None, None, None)
        self.choice_var.set("__reset__")

    def _build_create_user(self):
        frame = tk.Frame(self.content, bg="#f2f4f7")

        card = tk.Frame(frame, bg="#ffffff", padx=30, pady=24)
        card.pack(pady=40)

        tk.Label(
            card,
            text="Create New User",
            font=("TkDefaultFont", 13, "bold"),
            bg="#ffffff",
            fg="#1c2533"
        ).pack(pady=(0, 16))

        tk.Label(card, text="Email", bg="#ffffff").pack(anchor="w")
        self.create_email = tk.Entry(card, width=36)
        self.create_email.pack(pady=(0, 10))

        tk.Label(card, text="Temporary Password", bg="#ffffff").pack(anchor="w")
        self.create_password = tk.Entry(card, width=36, show="*")
        self.create_password.pack(pady=(0, 10))

        tk.Label(card, text="Name", bg="#ffffff").pack(anchor="w")
        self.create_name = tk.Entry(card, width=36)
        self.create_name.pack(pady=(0, 10))

        tk.Label(card, text="Role", bg="#ffffff").pack(anchor="w")
        self.create_role_var = tk.StringVar(value="warehouse_staff")
        role_menu = tk.OptionMenu(
            card,
            self.create_role_var,
            "admin",
            "manager",
            "driver",
            "warehouse_staff"
        )
        role_menu.config(width=28)
        role_menu.pack(pady=(0, 16))

        btn_row = tk.Frame(card, bg="#ffffff")
        btn_row.pack()

        tk.Button(
            btn_row,
            text="Create",
            width=14,
            command=self._submit_create_user
        ).pack(side=tk.LEFT, padx=6)

        tk.Button(
            btn_row,
            text="Back",
            width=14,
            command=self._cancel_create_user
        ).pack(side=tk.LEFT, padx=6)

        return frame

    def _build_profile(self):
        frame = tk.Frame(self.content, bg="#f2f4f7")

        card = tk.Frame(frame, bg="#ffffff", padx=30, pady=24)
        card.pack(pady=40)

        tk.Label(
            card,
            text="User Profile",
            font=("TkDefaultFont", 13, "bold"),
            bg="#ffffff",
            fg="#1c2533"
        ).pack(pady=(0, 16))

        self.profile_text = tk.Label(
            card,
            text="",
            justify="left",
            bg="#ffffff",
            fg="#2a3442",
            font=("TkDefaultFont", 11)
        )
        self.profile_text.pack(pady=(0, 16))

        tk.Button(
            card,
            text="Back",
            width=14,
            command=self._exit_profile
        ).pack()

        return frame

    def _exit_profile(self):
        self._profile_back.set(True)

    def _submit_create_user(self):
        self._create_user_result = (
            self.create_email.get().strip(),
            self.create_password.get().strip(),
            self.create_name.get().strip(),
            self.create_role_var.get().strip()
        )
        self.choice_var.set("__create__")

    def _cancel_create_user(self):
        self._create_user_result = (None, None, None, None)
        self.choice_var.set("__create__")

    def _wait_for_choice(self):
        self.root.wait_variable(self.choice_var)
        if self._closed:
            return "__exit__"
        return self.choice_var.get()

    def _set_status(self, text, style="info"):
        self._status_var.set(text)
        if style == "error":
            self.status_label.config(fg="#b42318")
        elif style == "success":
            self.status_label.config(fg="#067647")
        else:
            self.status_label.config(fg="#5a6779")

    def clear(self):
        self._set_status("")

    def show_header(self):
        self.header_title.config(text="Data Management System")

    def show_main_menu(self):
        self._set_status("Enter your credentials")
        self._set_nav_buttons([])
        self._show_page("login")

    def show_authenticated_menu_with_roles(self, user_name, user_role, is_admin):
        self._last_is_admin = is_admin
        self._set_status("Dashboard")
        self.auth_title.config(text=f"Role: {user_role.upper()} | User: {user_name}")
        self._rebuild_auth_menu_buttons()
        if is_admin:
            self._set_nav_buttons([
                ("Logout", "4")
            ])
        else:
            self._set_nav_buttons([
                ("Logout", "3")
            ])
        self._show_page("auth_menu")

    def get_login_input(self):
        result = self._login_result
        self._login_result = (None, None)
        return result

    def show_login_success(self, user):
        self._set_status("Login successful", "success")

    def show_login_failure(self):
        self._set_status("Login failed. Check your credentials.", "error")

    def show_profile(self, user):
        self.profile_text.config(
            text=(
                f"Name: {user['name']}\n"
                f"Email: {user['email']}\n"
                f"Role: {user['role'].upper()}\n"
                f"Created: {user['created_at']}\n"
                f"Active: {'Yes' if user['is_active'] else 'No'}"
            )
        )
        self._profile_back.set(False)
        self._show_page("profile")
        self.root.wait_variable(self._profile_back)

    def get_password_reset_input(self):
        self.current_password.delete(0, tk.END)
        self.new_password.delete(0, tk.END)
        self.confirm_password.delete(0, tk.END)
        self._set_status("Update your password")
        self._show_page("reset_password")
        choice = self._wait_for_choice()
        if choice == "__reset__":
            return self._password_reset_result
        if choice == "__exit__":
            return None, None, None
        return None, None, None

    def show_password_reset_result(self, success):
        if success:
            self._set_status("Password updated", "success")
        else:
            self._set_status("Password update failed", "error")

    def get_create_user_input(self):
        self.create_email.delete(0, tk.END)
        self.create_password.delete(0, tk.END)
        self.create_name.delete(0, tk.END)
        self.create_role_var.set("warehouse_staff")
        self._set_status("Enter user details")
        self._show_page("create_user")
        choice = self._wait_for_choice()
        if choice == "__create__":
            return self._create_user_result
        if choice == "__exit__":
            return None, None, None, None
        return None, None, None, None

    def show_create_user_result(self, success, message):
        if success:
            self._set_status(message, "success")
        else:
            self._set_status(message, "error")

    def show_logout_message(self):
        self._set_status("Logged out", "success")

    def show_exit_message(self):
        self._set_status("Closing application")

    def get_main_menu_choice(self):
        choice = self._wait_for_choice()
        if choice == "__exit__":
            return "2"
        return choice

    def get_authenticated_menu_choice(self):
        choice = self._wait_for_choice()
        if choice == "__exit__":
            return "5" if self._last_is_admin else "4"
        return choice

    def get_exit_confirmation(self):
        return True

    def show_invalid_option(self):
        self._set_status("Invalid option. Please try again.", "error")

    def show_error(self, message):
        self._set_status(message, "error")
