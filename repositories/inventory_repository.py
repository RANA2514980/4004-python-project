import logging
from db.connection import DatabaseConnection

logger = logging.getLogger(__name__)


class InventoryRepository:

    def __init__(self):
        self.db_conn = DatabaseConnection()

    def get_inventory(self, warehouse_id, product_id):
        try:
            query = '''
                SELECT * FROM inventory
                WHERE warehouse_id = ? AND product_id = ?
            '''
            results = self.db_conn.execute_query(query, (warehouse_id, product_id))
            if results:
                return dict(results[0])
            return None
        except Exception as e:
            logger.error(f"Error getting inventory: {e}")
            return None

    def list_inventory_by_warehouse(self, warehouse_id):
        try:
            query = '''
                SELECT i.*, p.sku, p.name
                FROM inventory i
                JOIN products p ON p.id = i.product_id
                WHERE i.warehouse_id = ?
            '''
            results = self.db_conn.execute_query(query, (warehouse_id,))
            return [dict(row) for row in results]
        except Exception as e:
            logger.error(f"Error listing inventory: {e}")
            return []

    def set_inventory(self, warehouse_id, product_id, quantity, reorder_level=0):
        try:
            query = '''
                INSERT INTO inventory (warehouse_id, product_id, quantity, reorder_level)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(warehouse_id, product_id)
                DO UPDATE SET quantity = excluded.quantity,
                              reorder_level = excluded.reorder_level,
                              updated_at = CURRENT_TIMESTAMP
            '''
            self.db_conn.execute_update(query, (warehouse_id, product_id, quantity, reorder_level))
            return True
        except Exception as e:
            logger.error(f"Error setting inventory: {e}")
            return False

    def adjust_inventory(self, warehouse_id, product_id, change_qty, movement_type, note, created_by):
        try:
            connection = self.db_conn.get_connection()
            cursor = connection.cursor()

            cursor.execute('''
                SELECT id, quantity FROM inventory
                WHERE warehouse_id = ? AND product_id = ?
            ''', (warehouse_id, product_id))
            row = cursor.fetchone()

            if row:
                inventory_id = row[0]
                current_qty = row[1]
            else:
                cursor.execute('''
                    INSERT INTO inventory (warehouse_id, product_id, quantity, reorder_level)
                    VALUES (?, ?, 0, 0)
                ''', (warehouse_id, product_id))
                inventory_id = cursor.lastrowid
                current_qty = 0

            new_qty = current_qty + change_qty
            cursor.execute('''
                UPDATE inventory SET quantity = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (new_qty, inventory_id))

            cursor.execute('''
                INSERT INTO inventory_movements (
                    warehouse_id, product_id, change_qty, movement_type, note, created_by
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (warehouse_id, product_id, change_qty, movement_type, note, created_by))

            connection.commit()
            return True
        except Exception as e:
            self.db_conn.get_connection().rollback()
            logger.error(f"Error adjusting inventory: {e}")
            return False
