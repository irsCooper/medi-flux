

from typing import Optional
import uuid
from pydantic import BaseModel, Field


class RefreshCreate(BaseModel):
    refresh_token: uuid.UUID
    access_token: str 
    expire_in: int 
    user_id: uuid.UUID

class RefreshUpdate(RefreshCreate):
    user_id: Optional[uuid.UUID] = Field(None)


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"