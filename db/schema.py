import logging
from db.connection import DatabaseConnection
from db.tables import TABLE_CREATORS
from db.tables import users_table
from db.tables import warehouses_table
from db.tables import products_table
from db.tables import inventory_table
from db.tables import inventory_movements_table

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
                'name': 'Administrator',
                'password': 'password',
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
        DatabaseSchema.initialize_default_data()
        logger.info("Database initialization complete")
