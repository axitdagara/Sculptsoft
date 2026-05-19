from __future__ import annotations
import os
import dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from config.exceptions import DatabaseError
from config.logger import get_logger
from sqlalchemy.orm import sessionmaker, declarative_base

dotenv.load_dotenv()     ## baki 


logger = get_logger(__name__)


def create_connection():
    logger.info("Creating raw database connection")
    host = os.getenv("host")
    user = os.getenv("user")
    password = os.getenv("password")
    database = os.getenv("database")
    port = os.getenv("port")

    
    required_vars = {"host": host, "user": user, "password": password, "database": database, "port": port}
    missing_vars = [key for key, value in required_vars.items() if not value]

    if missing_vars:
        error_msg = f"Missing required database configuration: {', '.join(missing_vars)}"
        logger.error(error_msg)
        raise DatabaseError(error_msg)

    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port,
    )

    return connection


def get_cursor(connection):
    return connection.cursor(cursor_factory=RealDictCursor)

#cursor = get_cursor(conn)
#cursor.execute("SELECT * FROM users")
# rows = curson.fetchall()
## results are in dict , not in tupple so , row ["id"]  , access coloums by name






Base = declarative_base()


def _build_sqlalchemy_url():
    host = os.getenv("host")
    user = os.getenv("user")
    password = os.getenv("password")
    database = os.getenv("database")
    port = os.getenv("port")

    required_vars = {"host": host, "user": user, "password": password, "database": database, "port": port}
    missing_vars = [key for key, value in required_vars.items() if not value]

    if missing_vars:
        error_msg = f"Missing required database configuration: {', '.join(missing_vars)}"
        logger.error(error_msg)
        raise DatabaseError(error_msg)

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"



_engine = None
_SessionLocal = None


def get_engine():
    global _engine
    if _engine is None:
        logger.info("Creating SQLAlchemy engine")
        url = _build_sqlalchemy_url()
        _engine = create_engine(url)
    return _engine


def get_session():
    
    global _SessionLocal
    if _SessionLocal is None:
        logger.info("Creating SQLAlchemy session factory")
        engine = get_engine()
        _SessionLocal = sessionmaker(bind=engine, autoflush=False)
    return _SessionLocal()
