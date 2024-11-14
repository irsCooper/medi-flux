from src.authentication.model import RefreshModel
from src.authentication.schemas import Refresh, RefreshCreate, RefreshUpdate
from src.base_dao import BaseDAO


class RefreshTokenDAO(BaseDAO[Refresh, RefreshCreate, RefreshUpdate]):
    model = RefreshModel