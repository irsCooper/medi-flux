from typing import List, Optional
import uuid
from pydantic import BaseModel, ConfigDict


ROLE_USER = "User"
ROLE_ADMIN = "Admin"
ROLE_MANAGER = "Manager"
ROLE_DOCTOR = "Doctor"


class UserBase(BaseModel):
    last_name: str 
    first_name: str 
    user_name: str 


class UserView(UserBase):
    roles: List[str]

# запись
class UserDB(UserBase):
    id: uuid.UUID
    hashed_password: bytes
    active: bool
    roles: List[str]
    model_config = ConfigDict(from_attributes=True)

# запрос
class UserCreate(UserBase):
    password: str

# запрос
class UserCreateDB(UserBase):
    hashed_password: bytes
    roles: List[str]

# запрос
class UserUpdate(BaseModel):
    last_name: str 
    first_name: str 
    password: str

# запрос
class UserUpdateDB(UserBase):
    user_name: Optional[str] = None
    hashed_password: bytes
    roles: Optional[List[str]] = None

# запрос
class UserCreateAdmin(UserCreate):
    roles: List[str]

# запрос
class UserUpdateAdmin(UserCreateAdmin):
    pass