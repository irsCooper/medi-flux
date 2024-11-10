import uuid
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.accounts.service import UserService
from src.accounts.dao import UserDAO
from src.accounts.schemas import UserView
from src.core.db_helper import db


router = APIRouter(
    prefix="/Accounts",
    tags=["Accounts"],
)


@router.get("/Me", response_model=UserView)
async def get_user_info(
    id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency)
):
    return await UserService.get_user(user_id=id, session=session)
    


@router.get("", response_model=list[UserView])
async def get_list_users(
    offset: int,
    count: int,
    session: AsyncSession = Depends(db.session_dependency)
):
    return await UserService.get_list_users(
        session=session,
        offset=offset, 
        limit=count, 
    )
