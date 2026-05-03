import logging
import sys
from pathlib import Path

from db.connection import DatabaseConnection
from db.schema import DatabaseSchema
from ui.tkinter_main import TkinterUIAdapter

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


def initialize_app():
    logger.info("=" * 60)
    logger.info("Starting Data Management System")
    logger.info("=" * 60)

    try:
        # DB connection (keep as-is)
        db_conn = DatabaseConnection()
        db_conn.connect()

        # schema init (keep as-is)
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
            print("\nPlease check logs for details.")
            return 1

        # 🔥 EVENT-DRIVEN ENTRY POINT
        ui = TkinterUIAdapter()
        ui.run()   # <-- this starts Tkinter mainloop

        # optional cleanup (only if you implemented disconnect)
        try:
            db_conn = DatabaseConnection()
            db_conn.disconnect()
        except:
            pass

        logger.info("Application shut down successfully")
        return 0

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\nFatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())