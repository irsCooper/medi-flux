from typing import List, Optional
import uuid
from pydantic import BaseModel, ConfigDict


class RoleSchema(BaseModel):
    name_role: str


class UserBase(BaseModel):
    last_name: str 
    first_name: str 
    user_name: str 


class UserView(UserBase):
    roles: List[RoleSchema]

# запись
class UserDB(UserBase):
    id: uuid.UUID
    hashed_password: bytes
    active: bool
    roles: List[RoleSchema]
    model_config = ConfigDict(from_attributes=True)

# запрос
class UserCreate(UserBase):
    password: str

# запрос
class UserCreateDB(UserBase):
    hashed_password: bytes
    roles: List[RoleSchema]

# запрос
class UserUpdate(BaseModel):
    last_name: str 
    first_name: str 
    password: str

# запрос
class UserUpdateDB(UserBase):
    user_name: Optional[str] = None
    hashed_password: bytes
    roles: Optional[List[RoleSchema]] = None

# запрос
class UserCreateAdmin(UserCreate):
    roles: List[RoleSchema]

# запрос
class UserUpdateAdmin(UserCreateAdmin):
    pass