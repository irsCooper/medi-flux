import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.rabbit_mq.account import AccountRabbitHelper
from src.history.service import HistoryService
from src.core.db_helper import db
from src.history.schemas import HistoryCreate, HistoryUpdate

router = APIRouter(
    prefix='/History',
    tags=['History']
)

@router.get("/Account/{id}")
async def get_history_of_visits_and_appointments_by_account(
    id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency),
    valid_token: str = Depends(AccountRabbitHelper.validate_token)
):  
    return await HistoryService.get_history_of_visits_and_appointments_by_account(
        account_id=id,
        token=valid_token,
        session=session
    )


@router.get("/{id}")
async def get_history_of_visits_and_appointments(
    id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency),
    valid_token: str = Depends(AccountRabbitHelper.validate_token)
):  
    return await HistoryService.get_history_of_visits_and_appointments(
        history_id=id,
        token=valid_token,
        session=session
    )


@router.post("")
async def create_history(
    history: HistoryCreate,
    session: AsyncSession = Depends(db.session_dependency)
):  
    return await HistoryService.create_history(
        history_create=history, 
        session=session
    )


@router.put("")
async def update_history(
    history: HistoryUpdate,
    session: AsyncSession = Depends(db.session_dependency)
):  
    return await HistoryService.update_history(
        history_update=history,
        session=session
    )