from fastapi import Depends
from sqlalchemy.orm import Session

from config.db import get_db
from services.library import Library


def get_library(db: Session = Depends(get_db)) -> Library:
    return Library(db)