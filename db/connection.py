import sqlite3
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseConnection:
    
    _instance = None
    _connection = None
    _db_path = None
    
    def __new__(cls, db_path="data.db"):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._db_path = db_path
        return cls._instance
    
    def connect(self):
        if self._connection is None:
            try:
                db_file = Path(self._db_path)
                db_file.parent.mkdir(parents=True, exist_ok=True)
                
                self._connection = sqlite3.connect(self._db_path)
                self._connection.row_factory = sqlite3.Row
                logger.info(f"Database connection established: {self._db_path}")
                return self._connection
            except sqlite3.Error as e:
                logger.error(f"Database connection error: {e}")
                raise
        return self._connection
    
    def disconnect(self):
        if self._connection:
            try:
                self._connection.close()
                self._connection = None
                logger.info("Database connection closed")
            except sqlite3.Error as e:
                logger.error(f"Error closing connection: {e}")
    
    def get_connection(self):
        if self._connection is None:
            return self.connect()
        return self._connection
    
    def execute_query(self, query, params=None):
        try:
            cursor = self._connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Query execution error: {e}")
            raise
    
    def execute_update(self, query, params=None):
        try:
            cursor = self._connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self._connection.commit()
            logger.debug(f"Rows affected: {cursor.rowcount}")
            return cursor.rowcount
        except sqlite3.Error as e:
            self._connection.rollback()
            logger.error(f"Update execution error: {e}")
            raise
    
    def __del__(self):
        self.disconnect()
