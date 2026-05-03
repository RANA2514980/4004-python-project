import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class UIAdapter(ABC):

    @abstractmethod
    def show_header(self):
        pass

    @abstractmethod
    def show_main_menu(self):
        pass

    @abstractmethod
    def show_authenticated_menu_with_roles(self, user_name, user_role, is_admin):
        pass

    @abstractmethod
    def get_login_input(self):
        pass

    @abstractmethod
    def show_login_success(self, user):
        pass

    @abstractmethod
    def show_login_failure(self):
        pass

    @abstractmethod
    def show_profile(self, user):
        pass

    @abstractmethod
    def get_password_reset_input(self):
        pass

    @abstractmethod
    def show_password_reset_result(self, success):
        pass

    @abstractmethod
    def get_create_user_input(self):
        pass

    @abstractmethod
    def show_create_user_result(self, success, message):
        pass

    @abstractmethod
    def show_logout_message(self):
        pass

    @abstractmethod
    def show_exit_message(self):
        pass

    @abstractmethod
    def get_main_menu_choice(self):
        pass

    @abstractmethod
    def get_authenticated_menu_choice(self):
        pass

    @abstractmethod
    def get_exit_confirmation(self):
        pass

    @abstractmethod
    def show_invalid_option(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def show_error(self, message):
        pass
