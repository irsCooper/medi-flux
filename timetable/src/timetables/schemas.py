import uuid
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TimetableSchema(BaseModel):
    id: uuid.UUID
    hospital_id: uuid.UUID
    doctor_id: uuid.UUID
    from_column: datetime
    to: datetime
    room: str

class TimetableDB(TimetableSchema):
    model_config = ConfigDict(from_attributes=True)

class TimetableCreate(BaseModel):
    hospital_id: uuid.UUID
    doctor_id: uuid.UUID
    from_column: datetime
    to: datetime
    room: str

class TimetableUpdate(TimetableCreate):
    id: uuid.UUID
