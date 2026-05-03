import logging
import hashlib
import secrets
from db.connection import DatabaseConnection

logger = logging.getLogger(__name__)


class UserRepository:
    
    def __init__(self):
        self.db_conn = DatabaseConnection()
    
    @staticmethod
    def hash_password(password, salt=None):
        if salt is None:
            salt = secrets.token_hex(32)
        
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return password_hash, salt
    
    @staticmethod
    def verify_password(password, password_hash, salt):
        computed_hash, _ = UserRepository.hash_password(password, salt)
        return computed_hash == password_hash
    
    def create_user(self, email, name, password, role):
        try:
            valid_roles = ['admin', 'manager', 'driver', 'warehouse_staff']
            if role not in valid_roles:
                logger.warning(f"Invalid role: {role}")
                return None
            
            password_hash, salt = self.hash_password(password)
            
            query = '''
                INSERT INTO users (email, name, password_hash, password_salt, role)
                VALUES (?, ?, ?, ?, ?)
            '''
            
            self.db_conn.execute_update(query, (email, name, password_hash, salt, role))
            logger.info(f"User created successfully: {email}")
            
            user = self.find_by_email(email)
            return user['id'] if user else None
            
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None
    
    def find_by_email(self, email):
        try:
            query = 'SELECT * FROM users WHERE email = ? AND is_active = 1'
            results = self.db_conn.execute_query(query, (email,))
            
            if results:
                return dict(results[0])
            return None
            
        except Exception as e:
            logger.error(f"Error finding user by email: {e}")
            return None
    
    def find_by_id(self, user_id):
        try:
            query = 'SELECT * FROM users WHERE id = ? AND is_active = 1'
            results = self.db_conn.execute_query(query, (user_id,))
            
            if results:
                return dict(results[0])
            return None
            
        except Exception as e:
            logger.error(f"Error finding user by ID: {e}")
            return None
    
    def get_all_users(self):
        try:
            query = 'SELECT id, email, name, role, created_at FROM users WHERE is_active = 1'
            results = self.db_conn.execute_query(query)
            return [dict(row) for row in results]
            
        except Exception as e:
            logger.error(f"Error retrieving all users: {e}")
            return []
    
    def update_user(self, user_id, **kwargs):
        try:
            allowed_fields = ['name', 'role', 'is_active']
            update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
            
            if not update_fields:
                logger.warning("No valid fields to update")
                return False
            
            set_clause = ', '.join([f'{field} = ?' for field in update_fields.keys()])
            values = list(update_fields.values())
            values.append(user_id)
            
            query = f'UPDATE users SET {set_clause} WHERE id = ?'
            self.db_conn.execute_update(query, values)
            
            logger.info(f"User {user_id} updated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return False

    def update_password(self, user_id, new_password):
        try:
            password_hash, salt = self.hash_password(new_password)
            query = 'UPDATE users SET password_hash = ?, password_salt = ? WHERE id = ?'
            self.db_conn.execute_update(query, (password_hash, salt, user_id))
            logger.info(f"Password updated for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating password: {e}")
            return False
    
    def deactivate_user(self, user_id):
        return self.update_user(user_id, is_active=False)
