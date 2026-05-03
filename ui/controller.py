import logging
from services.auth_service import AuthService

logger = logging.getLogger(__name__)


class UIController:

    def __init__(self, adapter):
        self.adapter = adapter
        self.auth_service = AuthService()

    def run(self):
        try:
            logger.info("Starting UI controller")
            self._run_main_menu()
        except KeyboardInterrupt:
            self.adapter.show_error("Application terminated by user")
        except Exception as e:
            self.adapter.show_error(f"Unexpected error: {e}")
            logger.error(f"UI error: {e}")

    def _run_main_menu(self):
        while True:
            self.adapter.clear()
            self.adapter.show_header()
            self.adapter.show_main_menu()

            choice = self.adapter.get_main_menu_choice()

            if choice == '1':
                if self._handle_login():
                    if not self._run_authenticated_menu():
                        continue
            elif choice == '2':
                self.adapter.clear()
                self.adapter.show_header()
                self.adapter.show_exit_message()
                return True
            else:
                self.adapter.clear()
                self.adapter.show_header()
                self.adapter.show_invalid_option()

    def _handle_login(self):
        self.adapter.clear()
        self.adapter.show_header()

        email, password = self.adapter.get_login_input()

        if not email or not password:
            self.adapter.clear()
            self.adapter.show_header()
            self.adapter.show_login_failure()
            return False

        user = self.auth_service.login(email, password)

        if user:
            self.adapter.clear()
            self.adapter.show_header()
            self.adapter.show_login_success(user)
            return True
        else:
            self.adapter.clear()
            self.adapter.show_header()
            self.adapter.show_login_failure()
            return False

    def _run_authenticated_menu(self):
        while True:
            user = self.auth_service.get_current_user()
            is_admin = self.auth_service.is_admin()
            self.adapter.clear()
            self.adapter.show_header()
            self.adapter.show_authenticated_menu_with_roles(user['name'], user['role'], is_admin)

            choice = self.adapter.get_authenticated_menu_choice()

            if choice == '1':
                self.adapter.clear()
                self.adapter.show_header()
                self.adapter.show_profile(user)
            elif choice == '2':
                self._handle_password_reset()
            elif choice == '3' and is_admin:
                self._handle_admin_create_user()
            elif (choice == '3' and not is_admin) or (choice == '4' and is_admin):
                self.auth_service.logout()
                self.adapter.clear()
                self.adapter.show_header()
                self.adapter.show_logout_message()
                return True
            elif (choice == '4' and not is_admin) or (choice == '5' and is_admin):
                confirm = self.adapter.get_exit_confirmation()
                if confirm:
                    return False
            else:
                self.adapter.clear()
                self.adapter.show_header()
                self.adapter.show_invalid_option()

    def _handle_password_reset(self):
        self.adapter.clear()
        self.adapter.show_header()
        current_password, new_password, confirm_password = self.adapter.get_password_reset_input()

        if not current_password or not new_password or not confirm_password:
            self.adapter.clear()
            self.adapter.show_header()
            self.adapter.show_password_reset_result(False)
            return

        if new_password != confirm_password:
            self.adapter.clear()
            self.adapter.show_header()
            self.adapter.show_password_reset_result(False)
            return

        success = self.auth_service.reset_own_password(current_password, new_password)
        self.adapter.clear()
        self.adapter.show_header()
        self.adapter.show_password_reset_result(success)

    def _handle_admin_create_user(self):
        self.adapter.clear()
        self.adapter.show_header()
        email, password, name, role = self.adapter.get_create_user_input()

        if not email or not password or not name or not role:
            self.adapter.clear()
            self.adapter.show_header()
            self.adapter.show_create_user_result(False, "All fields are required.")
            return

        user_id = self.auth_service.register_user(email, name, password, role)
        if user_id:
            self.adapter.clear()
            self.adapter.show_header()
            self.adapter.show_create_user_result(True, "User created successfully.")
        else:
            self.adapter.clear()
            self.adapter.show_header()
            self.adapter.show_create_user_result(False, "Failed to create user.")
