import uuid
from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from src.accounts.service import UserService
from src.accounts.dao import UserDAO
from src.accounts.schemas import UserCreateAdmin, UserDB, UserUpdate, UserView
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
    

@router.put("/Update")
async def update_user_info(
    user_id: uuid.UUID,
    user: UserUpdate,
    session: AsyncSession = Depends(db.session_dependency)
):
    return await UserService.update_user(user_id=user_id, user=user, session=session)


@router.get("/", response_model=list[UserView])
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


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_only_admin(
    user: UserCreateAdmin,
    session: AsyncSession = Depends(db.session_dependency)
):
    await UserService.create_user(
        user_in=user,
        session=session,
    )
    return {
        "status_code": status.HTTP_201_CREATED,
        "detail": "User created",
    }