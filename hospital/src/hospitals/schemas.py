from typing import List
from pydantic import BaseModel, ConfigDict

import uuid


class RoomSchema(BaseModel):
    name: str 


class HospitalSchema(BaseModel):
    id: uuid.UUID
    name: str
    address: str
    contactPhone: str
    rooms: List[RoomSchema]


class HospitalDB(HospitalSchema):
    is_deleted: bool = False
    model_config = ConfigDict(from_attributes=True)


class HospitalCreate(BaseModel):
    name: str
    address: str
    contactPhone: str
    rooms: List[RoomSchema]


class HospitalUpdate(HospitalCreate):
    id: uuid.UUID