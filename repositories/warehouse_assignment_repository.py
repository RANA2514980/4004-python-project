import logging
from db.connection import DatabaseConnection

logger = logging.getLogger(__name__)


class WarehouseAssignmentRepository:

    def __init__(self):
        self.db = DatabaseConnection()

    # ---------------- ASSIGN SINGLE USER ----------------

    def assign_user(self, user_id, warehouse_id):
        try:
            query = """
                INSERT INTO warehouse_staff_assignment (user_id, warehouse_id)
                VALUES (?, ?)
                ON CONFLICT(user_id)
                DO UPDATE SET
                    warehouse_id = excluded.warehouse_id,
                    assigned_at = CURRENT_TIMESTAMP
            """
            self.db.execute_update(query, (user_id, warehouse_id))
            return True

        except Exception as e:
            print("Assign error:", e)
            return False

    # ---------------- UNASSIGNED STAFF ----------------

    def get_unassigned_staff(self):
        query = """
            SELECT u.*
            FROM users u
            LEFT JOIN warehouse_staff_assignment w
            ON u.id = w.user_id
            WHERE w.user_id IS NULL
            AND u.role = 'warehouse_staff'
            AND u.is_active = 1
        """
        return [dict(r) for r in self.db.execute_query(query)]

    # ---------------- ASSIGNED STAFF ----------------

    def get_assigned_staff(self, warehouse_id):
        try:
            query = """
                SELECT u.*
                FROM users u
                JOIN warehouse_staff_assignment w
                ON u.id = w.user_id
                WHERE w.warehouse_id = ?
            """
            return [dict(r) for r in self.db.execute_query(query, (warehouse_id,))]

        except Exception as e:
            logger.error(f"Assigned staff error: {e}")
            return []

    # ---------------- REMOVE ASSIGNMENT ----------------

    def remove_assignment(self, user_id):
        try:
            query = """
                DELETE FROM warehouse_staff_assignment
                WHERE user_id = ?
            """
            self.db.execute_update(query, (user_id,))
            return True

        except Exception as e:
            logger.error(f"Remove assignment error: {e}")
            return False