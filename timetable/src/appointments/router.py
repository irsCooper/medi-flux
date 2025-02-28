import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.appointments.service import AppointmentsService
from src.core.db_helper import db
from src.core.config import ROLE_ADMIN, ROLE_MANAGER
from src.rabbit_mq.account import AccountRabbitHelper

router = APIRouter(
    prefix='/Appointments',
    tags=['Appointment']
)

@router.delete("/{id}")
async def delete_appointments(
    id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency),
    valid_token: str = Depends(AccountRabbitHelper.validate_token)
):
    await AppointmentsService.check_role_or_exists_appointment(
        roles=[ROLE_ADMIN, ROLE_MANAGER], 
        token=valid_token, 
        appointnment_id=id
    )

    await AppointmentsService.delete_appoointment(
        appointment_id=id,
        session=session
    )