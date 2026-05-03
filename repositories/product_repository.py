import logging
from db.connection import DatabaseConnection

logger = logging.getLogger(__name__)


class ProductRepository:

    def __init__(self):
        self.db_conn = DatabaseConnection()

    def create_product(self, sku, name, description=None, unit='unit'):
        try:
            query = '''
                INSERT INTO products (sku, name, description, unit)
                VALUES (?, ?, ?, ?)
            '''
            self.db_conn.execute_update(query, (sku, name, description, unit))
            logger.info(f"Product created: {sku}")
            return True
        except Exception as e:
            logger.error(f"Error creating product: {e}")
            return False

    def list_products(self, active_only=True):
        try:
            if active_only:
                query = 'SELECT * FROM products WHERE is_active = 1'
                results = self.db_conn.execute_query(query)
            else:
                query = 'SELECT * FROM products'
                results = self.db_conn.execute_query(query)
            return [dict(row) for row in results]
        except Exception as e:
            logger.error(f"Error listing products: {e}")
            return []

    def find_by_sku(self, sku):
        try:
            query = 'SELECT * FROM products WHERE sku = ? AND is_active = 1'
            results = self.db_conn.execute_query(query, (sku,))
            if results:
                return dict(results[0])
            return None
        except Exception as e:
            logger.error(f"Error finding product: {e}")
            return None

    def update_product(self, product_id, **kwargs):
        try:
            allowed_fields = ['sku', 'name', 'description', 'unit', 'is_active']
            update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
            if not update_fields:
                return False
            set_clause = ', '.join([f'{field} = ?' for field in update_fields.keys()])
            values = list(update_fields.values())
            values.append(product_id)
            query = f'UPDATE products SET {set_clause} WHERE id = ?'
            self.db_conn.execute_update(query, values)
            logger.info(f"Product updated: {product_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating product: {e}")
            return False
