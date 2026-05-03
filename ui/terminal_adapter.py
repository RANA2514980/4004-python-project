import logging
import os
from ui.adapter import UIAdapter

logger = logging.getLogger(__name__)


class TerminalUIAdapter(UIAdapter):

    def clear(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def show_header(self):
        print("\n" + "="*60)
        print(" "*15 + "DATA MANAGEMENT SYSTEM")
        print("="*60 + "\n")

    def show_main_menu(self):
        print("\n" + "-"*60)
        print("MAIN MENU")
        print("-"*60)
        print("1. Login")
        print("2. Exit")
        print("-"*60)

    def show_authenticated_menu_with_roles(self, user_name, user_role, is_admin):
        print("\n" + "-"*60)
        print(f"LOGGED IN AS: {user_name} ({user_role.upper()})")
        print("-"*60)
        print("1. View Profile")
        print("2. Reset Password")
        if is_admin:
            print("3. Create New User")
            print("4. Logout")
            print("5. Exit")
        else:
            print("3. Logout")
            print("4. Exit")
        print("-"*60)

    def get_login_input(self):
        print("LOGIN")
        print("-"*60)

        try:
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            return email, password
        except KeyboardInterrupt:
            raise
        except Exception as e:
            logger.error(f"Input error: {e}")
            return None, None

    def show_login_success(self, user):
        print("✓ LOGIN SUCCESSFUL!")
        print("-"*60)
        print(f"Welcome, {user['name']}!")
        print(f"Role: {user['role'].upper()}")
        print(f"Email: {user['email']}")
        print("-"*60)
        input("\nPress Enter to continue...")

    def show_login_failure(self):
        print("❌ LOGIN FAILED!")
        print("-"*60)
        print("Invalid email or password. Please try again.")
        print("-"*60)
        input("\nPress Enter to continue...")

    def show_profile(self, user):
        print("USER PROFILE")
        print("-"*60)
        print(f"Name:         {user['name']}")
        print(f"Email:        {user['email']}")
        print(f"Role:         {user['role'].upper()}")
        print(f"Created:      {user['created_at']}")
        print(f"Active:       {'Yes' if user['is_active'] else 'No'}")
        print("-"*60)
        input("\nPress Enter to continue...")

    def get_password_reset_input(self):
        print("RESET PASSWORD")
        print("-"*60)
        current_password = input("Current Password: ").strip()
        new_password = input("New Password: ").strip()
        confirm_password = input("Confirm New Password: ").strip()
        return current_password, new_password, confirm_password

    def show_password_reset_result(self, success):
        if success:
            print("✓ PASSWORD UPDATED")
            print("-"*60)
            print("Your password has been updated.")
        else:
            print("❌ PASSWORD UPDATE FAILED")
            print("-"*60)
            print("Password update failed. Check your inputs and try again.")
        print("-"*60)
        input("\nPress Enter to continue...")

    def get_create_user_input(self):
        print("CREATE NEW USER")
        print("-"*60)
        email = input("Email: ").strip()
        password = input("Temporary Password: ").strip()
        name = input("Name: ").strip()
        role = input("Role (admin/manager/driver/warehouse_staff): ").strip()
        return email, password, name, role

    def show_create_user_result(self, success, message):
        if success:
            print("✓ USER CREATED")
        else:
            print("❌ USER CREATION FAILED")
        print("-"*60)
        print(message)
        print("-"*60)
        input("\nPress Enter to continue...")

    def show_logout_message(self):
        print("✓ LOGGED OUT SUCCESSFULLY")
        print("-"*60)
        print("You have been logged out.")
        print("-"*60)
        input("\nPress Enter to continue...")

    def show_exit_message(self):
        print("Thank you for using Data Management System!")
        print("-"*60)

    def get_main_menu_choice(self):
        return input("Select option: ").strip()

    def get_authenticated_menu_choice(self):
        return input("Select option: ").strip()

    def get_exit_confirmation(self):
        confirm = input("\nAre you sure you want to exit? (yes/no): ").strip().lower()
        return confirm == 'yes'

    def show_invalid_option(self):
        print("❌ Invalid option. Please try again.")
        input("\nPress Enter to continue...")

    def show_error(self, message):
        print(f"\n❌ {message}")
