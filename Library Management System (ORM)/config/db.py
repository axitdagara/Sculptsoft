from __future__ import annotations
import os
import dotenv
from sqlalchemy import create_engine
from exceptions import DatabaseError
from sqlalchemy.orm import sessionmaker, declarative_base

dotenv.load_dotenv()



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
        raise DatabaseError(error_msg)

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"


def get_database_url():
    return _build_sqlalchemy_url()


_engine = None
_SessionLocal = None


def get_engine():
    global _engine
    if _engine is None:
        url = _build_sqlalchemy_url()
        _engine = create_engine(url, future=True)
    return _engine


def get_session_factory():
    global _SessionLocal
    if _SessionLocal is None:
        engine = get_engine()
        _SessionLocal = sessionmaker(bind=engine, autoflush=False, future=True)
    return _SessionLocal


def get_session():
    """Return a new SQLAlchemy Session."""
    session_factory = get_session_factory()
    return session_factory()


def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()
