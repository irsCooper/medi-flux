

from typing import List
import uuid
from pydantic import BaseModel, ConfigDict


class RoomSchema(BaseModel):
    name: str 


class HospitalSchema(BaseModel):
    id: uuid.UUID
    name: str
    addresss: str
    contactPhone: str
    rooms: List[RoomSchema]


class HospitalDB(HospitalSchema):
    model_config = ConfigDict(from_attributes=True)


class HospitalCreate(BaseModel):
    name: str
    addresss: str
    contactPhone: str
    rooms: List[RoomSchema]


class HospitalUpdate(HospitalCreate):
    id: uuid.UUID