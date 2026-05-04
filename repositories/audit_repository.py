import logging
from db.connection import DatabaseConnection

logger = logging.getLogger(__name__)


class AuditRepository:
    def __init__(self):
        self.db = DatabaseConnection()

    def create_log(self, user_id, action, entity_type, entity_id=None, details=None):
        query = """
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
            VALUES (?, ?, ?, ?, ?)
        """
        try:
            self.db.execute_update(query, (user_id, action, entity_type, entity_id, details))
            return True
        except Exception as e:
            logger.error(f"Audit log error: {e}")
            return False
