from sqlalchemy import select
from src.base_dao import BaseDAO
from src.history.schemas import HistoryCreate, HistoryUpdate
from src.history.model import HistoryModel

class HistoryDAO(BaseDAO[HistoryModel, HistoryCreate, HistoryUpdate]):
    model = HistoryModel