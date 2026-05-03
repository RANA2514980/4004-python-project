import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from db.connection import DatabaseConnection
from db.schema import DatabaseSchema
from ui.controller import UIController
from ui.tkinter_adapter import TkinterUIAdapter


def initialize_app():
    logger.info("="*60)
    logger.info("Starting Data Management System")
    logger.info("="*60)
    
    try:
        db_conn = DatabaseConnection()
        db_conn.connect()
        
        DatabaseSchema.initialize_database()
        
        logger.info("Application initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        print(f"\nFailed to initialize application: {e}")
        return False


def main():
    try:
        if not initialize_app():
            print("\nPlease check the logs for more details.")
            return 1
        
        adapter = TkinterUIAdapter()
        controller = UIController(adapter)
        controller.run()
        
        db_conn = DatabaseConnection()
        db_conn.disconnect()
        
        logger.info("Application shut down successfully")
        return 0
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\nFatal error: {e}")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
