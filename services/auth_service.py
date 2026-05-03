import logging
from repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class AuthService:
    
    def __init__(self):
        self.user_repo = UserRepository()
        self.current_user = None
    
    def login(self, email, password):
        try:
            user = self.user_repo.find_by_email(email)
            
            if not user:
                logger.warning(f"Login attempt with non-existent email: {email}")
                return None
            
            if not UserRepository.verify_password(
                password,
                user['password_hash'],
                user['password_salt']
            ):
                logger.warning(f"Failed login attempt for user: {email}")
                return None
            
            self.current_user = user
            logger.info(f"User logged in successfully: {email}")
            return user
            
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return None
    
    def logout(self):
        if self.current_user:
            logger.info(f"User logged out: {self.current_user['email']}")
            self.current_user = None
            return True
        return False
    
    def is_authenticated(self):
        return self.current_user is not None
    
    def get_current_user(self):
        return self.current_user
    
    def has_role(self, role):
        if not self.current_user:
            return False
        return self.current_user['role'] == role
    
    def has_roles(self, roles):
        if not self.current_user:
            return False
        return self.current_user['role'] in roles
    
    def is_admin(self):
        return self.has_role('admin')
    
    def require_role(self, role):
        if not self.has_role(role):
            raise PermissionError(f"User does not have required role: {role}")
        return True
    
    def register_user(self, email, name, password, role='warehouse_staff'):
        if not self.is_admin():
            logger.warning(f"Non-admin user attempted to register new user")
            return None
        
        return self.user_repo.create_user(email, name, password, role)

    def reset_own_password(self, current_password, new_password):
        if not self.current_user:
            return False

        if not UserRepository.verify_password(
            current_password,
            self.current_user['password_hash'],
            self.current_user['password_salt']
        ):
            logger.warning(f"Password reset failed for user: {self.current_user['email']}")
            return False

        updated = self.user_repo.update_password(self.current_user['id'], new_password)
        if updated:
            refreshed = self.user_repo.find_by_id(self.current_user['id'])
            if refreshed:
                self.current_user = refreshed
            logger.info(f"Password reset successful for user: {self.current_user['email']}")
        return updated
