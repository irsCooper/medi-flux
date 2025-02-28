import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# from src.documents.service import AppointmentsService
from src.core.db_helper import db
from src.core.config import ROLE_ADMIN, ROLE_MANAGER
from src.history.schemas import HistoryCreate, HistoryUpdate
# from src.rabbit_mq.account import AccountRabbitHelper

router = APIRouter(
    prefix='/History',
    tags=['History']
)

@router.get("/Account/{id}")
async def get_history_of_visits_and_appointments_by_account(
    id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency)
):  
    pass


@router.get("/{id}")
async def get_history_of_visits_and_appointments(
    id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency)
):  
    pass


@router.post("")
async def create_history(
    history: HistoryCreate,
    session: AsyncSession = Depends(db.session_dependency)
):  
    pass


@router.put("")
async def update_history(
    history: HistoryUpdate,
    session: AsyncSession = Depends(db.session_dependency)
):  
    pass