from repositories.audit_repository import AuditRepository


class AuditService:
    def __init__(self, auth_service):
        self.auth = auth_service
        self.repo = AuditRepository()

    def log(self, action, entity_type, entity_id=None, details=None):
        user = self.auth.get_current_user()
        user_id = user["id"] if user else None
        return self.repo.create_log(user_id, action, entity_type, entity_id, details)
