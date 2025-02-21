import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.appointments.service import AppointmentsService
from src.core.db_helper import db

router = APIRouter(
    prefix='/Appointments',
    tags=['Appointment']
)

@router.delete("/{id}")
async def delete_appointments(
    id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency)
):
    await AppointmentsService.delete_appoointment(
        appointment_id=id,
        session=session
    )