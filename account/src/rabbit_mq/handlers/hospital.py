import uuid
from src.core.db_helper import db
from src.doctors.service import DoctorSrvice
from src.accounts.service import UserService

from fastapi.exceptions import HTTPException

async def check_doctor_handler(doctor_id: str) -> bytes:
    try:
        async with db.session_dependency() as session:
            doctor = await DoctorSrvice.get_doctor(uuid.UUID(doctor_id), session)
            return b'\x01'
    except HTTPException:
        return b'\x00'

async def check_pacient_handler(user_id: str) -> bytes:
    try:
        async with db.session_dependency() as session:
            user = await UserService.get_user(uuid.UUID(user_id), session)
            return b'\x00' if 'User' not in [role.name_role for role in user.roles] else b'\x01'
    except HTTPException:
        return b'\x00'