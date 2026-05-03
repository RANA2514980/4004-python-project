import logging
from repositories.warehouse_assignment_repository import WarehouseAssignmentRepository

logger = logging.getLogger(__name__)


class WarehouseAssignmentService:

    def __init__(self, auth_service):
        self.auth = auth_service
        self.repo = WarehouseAssignmentRepository()

    def _require_admin(self):
        user = self.auth.get_current_user()
        if not user or user["role"] != "admin":
            return None
        return user

    def assign_users(self, warehouse_id, user_ids):
        if not self._require_admin():
            return False

        for uid in user_ids:
            self.repo.assign_user(uid, warehouse_id)

        return True

    def get_unassigned_staff(self):
        return self.repo.get_unassigned_staff()

    def get_assigned_staff(self, warehouse_id):
        return self.repo.get_assigned_staff(warehouse_id)

    def remove_assignment(self, user_id):
        if not self._require_admin():
            return False
        return self.repo.remove_assignment(user_id)