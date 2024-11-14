from datetime import datetime
import uuid
from sqlalchemy import TIMESTAMP, UUID, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.accounts.model import UserModel
from src.base_model import BaseModel

class RefreshModel(BaseModel):
    __tablename__ = 'refresh_session'

    reftesh_token: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True)
    access_token: Mapped[str]
    expire_in: Mapped[int]
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id", ondelete="CASCADE"))
    creates_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    user: Mapped[UserModel] = relationship("UserModel", back_populates="refresh_session")