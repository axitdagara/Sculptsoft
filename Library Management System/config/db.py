from __future__ import annotations
import os
import logging
import dotenv
import psycopg2
from psycopg2 import OperationalError, DatabaseError
from psycopg2.extras import RealDictCursor
from config.exceptions import ConnectionException

dotenv.load_dotenv()
logger = logging.getLogger(__name__)


def create_connection():

    try:
        host = os.getenv("host")
        user = os.getenv("user")
        password = os.getenv("password")
        database = os.getenv("database")
        port = os.getenv("port")
        
        # Validate required environment variables
        required_vars = {"host": host, "user": user, "password": password, "database": database, "port": port}
        missing_vars = [key for key, value in required_vars.items() if not value]
        
        if missing_vars:
            error_msg = f"Missing required database configuration: {', '.join(missing_vars)}"
            logger.error(error_msg)
            raise ConnectionException(error_msg)
        
        logger.debug(f"Attempting to connect to PostgreSQL at {host}:{port}")
        
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        
        logger.info(f"Successfully connected to PostgreSQL database: {database}")
        return connection

    except (OperationalError, DatabaseError) as e:
        error_msg = f"Database connection error: {str(e)}"
        logger.error(error_msg)
        raise ConnectionException(error_msg) from e
    except Exception as e:
        error_msg = f"Unexpected error while connecting to PostgreSQL: {str(e)}"
        logger.error(error_msg)
        raise ConnectionException(error_msg) from e


def get_cursor(connection):
    """Get a RealDictCursor from a database connection."""
    try:
        logger.debug("Creating RealDictCursor")
        return connection.cursor(cursor_factory=RealDictCursor)
    except Exception as e:
        logger.error(f"Failed to create cursor: {str(e)}")
        raise
