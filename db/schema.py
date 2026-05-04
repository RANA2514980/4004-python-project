import logging
from db.connection import DatabaseConnection
from db.tables import TABLE_CREATORS
from db.tables import users_table
from db.tables import warehouses_table
from db.tables import products_table
from db.tables import inventory_table
from db.tables import inventory_movements_table
from db.tables import shipments_table
from db.tables import vehicles_table
from db.tables import shipment_incidents_table
from db.tables import audit_logs_table

from db.tables.warehouse_staff_assignment_table import create_warehouse_staff_assignment_table

logger = logging.getLogger(__name__)


class DatabaseSchema:
    
    @staticmethod
    def create_tables():
        db_conn = DatabaseConnection()
        connection = db_conn.get_connection()
        
        try:
            for creator in TABLE_CREATORS:
                creator(connection)
            
            connection.commit()
            logger.info("Database tables created successfully")
            
        except Exception as e:
            connection.rollback()
            logger.error(f"Error creating tables: {e}")
            raise
    
    @staticmethod
    def initialize_default_data():
        from repositories.user_repository import UserRepository
        
        db_conn = DatabaseConnection()
        
        try:
            user_repo = UserRepository()
            existing_admin = user_repo.find_by_email('admin@gmail.com')
            
            if existing_admin:
                logger.info("Admin user already exists")
                return
            
            admin_data = {
                'email': 'admin@gmail.com',
                'name': 'admin',
                'password': 'pass',
                'role': 'admin'
            }
            
            user_repo.create_user(**admin_data)
            logger.info("Default admin user created successfully")
            
        except Exception as e:
            logger.error(f"Error initializing default data: {e}")
            raise
    
    @staticmethod
    def initialize_database():
        logger.info("Initializing database...")
        DatabaseSchema.create_tables()
        DatabaseSchema.ensure_schema_updates()
        DatabaseSchema.create_indexes()
        DatabaseSchema.initialize_default_data()
        logger.info("Database initialization complete")

    @staticmethod
    def ensure_schema_updates():
        db_conn = DatabaseConnection()
        connection = db_conn.get_connection()
        cursor = connection.cursor()

        def columns_for(table_name):
            cursor.execute(f"PRAGMA table_info({table_name})")
            return {row[1] for row in cursor.fetchall()}

        try:
            # Users table extensions
            user_cols = columns_for("users")
            if "driver_license" not in user_cols:
                cursor.execute("ALTER TABLE users ADD COLUMN driver_license TEXT")
            if "driver_phone" not in user_cols:
                cursor.execute("ALTER TABLE users ADD COLUMN driver_phone TEXT")
            if "driver_address" not in user_cols:
                cursor.execute("ALTER TABLE users ADD COLUMN driver_address TEXT")

            # Shipments table extensions
            shipment_cols = columns_for("shipments")
            if "order_number" not in shipment_cols:
                cursor.execute("ALTER TABLE shipments ADD COLUMN order_number TEXT")
            if "receiver_phone" not in shipment_cols:
                cursor.execute("ALTER TABLE shipments ADD COLUMN receiver_phone TEXT")
            if "payment_reference" not in shipment_cols:
                cursor.execute("ALTER TABLE shipments ADD COLUMN payment_reference TEXT")
            if "delivery_date" not in shipment_cols:
                cursor.execute("ALTER TABLE shipments ADD COLUMN delivery_date TEXT")
            if "route_details" not in shipment_cols:
                cursor.execute("ALTER TABLE shipments ADD COLUMN route_details TEXT")
            if "updated_at" not in shipment_cols:
                cursor.execute("ALTER TABLE shipments ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")

            # Vehicles table extensions
            vehicle_cols = columns_for("vehicles")
            if "last_service_date" not in vehicle_cols:
                cursor.execute("ALTER TABLE vehicles ADD COLUMN last_service_date TEXT")
            if "maintenance_due_date" not in vehicle_cols:
                cursor.execute("ALTER TABLE vehicles ADD COLUMN maintenance_due_date TEXT")

            connection.commit()
            logger.info("Schema updates applied")
        except Exception as e:
            connection.rollback()
            logger.error(f"Schema update error: {e}")
            raise

    @staticmethod
    def create_indexes():
        db_conn = DatabaseConnection()
        connection = db_conn.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_shipments_status ON shipments(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_shipments_driver ON shipments(assigned_driver_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_inventory_warehouse ON inventory(warehouse_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_inventory_product ON inventory(product_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_vehicles_status ON vehicles(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_entity ON audit_logs(entity_type, entity_id)")
            connection.commit()
            logger.info("Indexes ensured")
        except Exception as e:
            connection.rollback()
            logger.error(f"Index creation error: {e}")
            raise
