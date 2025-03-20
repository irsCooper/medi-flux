import uuid
from datetime import datetime
from pydantic import BaseModel


class HistoryCreate(BaseModel):
    date: datetime
    pacient_id: uuid.UUID
    hospital_id: uuid.UUID
    doctor_id: uuid.UUID
    room: str 
    data: str = None

class HistoryUpdate(HistoryCreate):
    id: uuid.UUID