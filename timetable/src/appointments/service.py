import uuid
from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.appointments.dao import AppointmentDAO, AppointmentModel
from src.rabbit_mq.account import AccountRabbitHelper

class AppointmentsService:
    @classmethod
    async def delete_appoointment(
        cls,
        appointment_id: uuid.UUID,
        session: AsyncSession
    ):
        await AppointmentDAO.delete(
            session,
            AppointmentModel.id == appointment_id
        )

    @classmethod
    async def check_role_or_exists_appointment(
        cls,
        roles: list,
        token: str,
        appointnment_id: uuid.UUID,
        sesssion: AsyncSession
    ):
        try:
            await AccountRabbitHelper.get_current_role(roles, token)
        except:
            decoded: dict = await AccountRabbitHelper.decoded_token(token)

            appointment = await AppointmentDAO.find_one_or_none(
                sesssion,
                and_(
                    AppointmentModel.id == appointnment_id,
                    AppointmentModel.user_id == decoded.get('sub')
                )
            )

            if not appointment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="You don't have an appointment for this appointment"
                )