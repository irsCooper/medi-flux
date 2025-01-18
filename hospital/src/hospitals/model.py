import uuid
from sqlalchemy import UUID, Boolean, ForeignKey, Integer, String
from ..base_model import BaseModel

from sqlalchemy.orm import Mapped, mapped_column, relationship


class HospitalRoomsModel(BaseModel):
    __tablename__ = 'hospital_rooms'

    hospital_id: Mapped[int] = mapped_column(ForeignKey("hospitals.id", ondelete="CASCADE"), primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id",  ondelete="CASCADE"), primary_key=True)


class RoomModel(BaseModel):
    __tablename__ = 'rooms'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)

    hospitals: Mapped[list["HospitalModel"]] = relationship(
        "HospitalModel",
        secondary="hospital_rooms",
        back_populates="rooms",
        cascade="all, delete",
        passive_deletes=True
    )


class HospitalModel(BaseModel):
    __tablename__ = 'hospitals'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String, nullable=False)
    contactPhone: Mapped[str] = mapped_column(String(300), nullable=False, unique=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    rooms: Mapped[list["RoomModel"]] = relationship(
        "RoomModel",
        secondary="hospital_rooms",
        back_populates="hospitals",
    )