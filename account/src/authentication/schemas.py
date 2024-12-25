from typing import Optional
import uuid
from fastapi import Form
from pydantic import BaseModel, Field


class RefreshCreate(BaseModel):
    user_id: uuid.UUID
    reftesh_token_id: uuid.UUID
    reftesh_token: str 
    access_token: str 
    expire_in: int 


class RefreshUpdate(RefreshCreate):
    user_id: Optional[uuid.UUID] = Field(None)


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class Refresh(BaseModel):
    refresh_token: uuid.UUID


class CredentialsForm(BaseModel):
    username: str = Form()
    password: str = Form()


class Credentials(BaseModel):
    username: str 
    password: str 