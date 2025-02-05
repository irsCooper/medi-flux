__all__ = (
    "db",
    "BaseModel",
    "DatabaseHelper",
    "settings",
    "Timetable"
)

from src.timetables.model import Timetable

from src.base_model import BaseModel
from src.core.db_helper import db, DatabaseHelper, settings