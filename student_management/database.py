from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import logging

# SQLite Database URL
DATABASE_URL = "sqlite:///student_management.db"

# Engine Create
engine = create_engine(
    DATABASE_URL,
    echo=False
)

# Silence verbose SQLAlchemy engine logging to keep console output clean
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

# Session Factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# Base Class
Base = declarative_base()

# Dependency function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()