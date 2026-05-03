import logging
from db.connection import DatabaseConnection

logger = logging.getLogger(__name__)


class WarehouseRepository:

    def __init__(self):
        self.db_conn = DatabaseConnection()

    def create_warehouse(self, name, location, status='active'):
        try:
            query = '''
                INSERT INTO warehouses (name, location, status)
                VALUES (?, ?, ?)
            '''
            self.db_conn.execute_update(query, (name, location, status))
            logger.info(f"Warehouse created: {name}")
            return True
        except Exception as e:
            logger.error(f"Error creating warehouse: {e}")
            return False

    def list_warehouses(self, active_only=True):
        try:
            if active_only:
                query = 'SELECT * FROM warehouses WHERE is_active = 1'
                results = self.db_conn.execute_query(query)
            else:
                query = 'SELECT * FROM warehouses'
                results = self.db_conn.execute_query(query)
            return [dict(row) for row in results]
        except Exception as e:
            logger.error(f"Error listing warehouses: {e}")
            return []

    def find_by_id(self, warehouse_id):
        try:
            query = 'SELECT * FROM warehouses WHERE id = ? AND is_active = 1'
            results = self.db_conn.execute_query(query, (warehouse_id,))
            if results:
                return dict(results[0])
            return None
        except Exception as e:
            logger.error(f"Error finding warehouse: {e}")
            return None

    def update_warehouse(self, warehouse_id, **kwargs):
        try:
            allowed_fields = ['name', 'location', 'status', 'is_active']
            update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
            if not update_fields:
                return False
            set_clause = ', '.join([f'{field} = ?' for field in update_fields.keys()])
            values = list(update_fields.values())
            values.append(warehouse_id)
            query = f'UPDATE warehouses SET {set_clause} WHERE id = ?'
            self.db_conn.execute_update(query, values)
            logger.info(f"Warehouse updated: {warehouse_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating warehouse: {e}")
            return False
