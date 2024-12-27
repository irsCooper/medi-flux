import uuid
from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from src.accounts.model import UserModel
from src.accounts.service import UserService
from src.accounts.schemas import UserCreateAdmin, UserDB, UserUpdate, UserView
from src.core.db_helper import db
from src.dependencies import get_current_auth_user, http_bearer


router = APIRouter(
    prefix="/Accounts",
    tags=["Accounts"],
    dependencies=[Depends(http_bearer)]
)


@router.get("/Me", response_model=UserView)
async def get_user_info(
    # id: uuid.UUID,
    user: UserModel = Depends(get_current_auth_user),
    session: AsyncSession = Depends(db.session_dependency)
):
    return await UserService.get_user(user_id=user.id, session=session)
    

@router.put("/Update", response_model=UserDB)
async def update_user_info(
    # user_id: uuid.UUID,
    user_update: UserUpdate,
    user: UserModel = Depends(get_current_auth_user),
    session: AsyncSession = Depends(db.session_dependency)
):
    return await UserService.update_user(user_id=user.id, user=user_update, session=session)


@router.get("", response_model=list[UserView])
async def get_list_users(
    offset: int,
    count: int,
    user: UserModel = Depends(get_current_auth_user),
    session: AsyncSession = Depends(db.session_dependency)
):
    return await UserService.get_list_users(
        session=session,
        offset=offset, 
        limit=count, 
        user=user
    )


@router.post("", status_code=status.HTTP_201_CREATED)
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


@router.put("/{id}", response_model=UserDB)
async def update_user_info_only_admin(
    id: uuid.UUID,
    user: UserUpdate,
    session: AsyncSession = Depends(db.session_dependency)
):
    return await UserService.update_user(user_id=id, user=user, session=session)



@router.delete("/{id}")
async def delete_user_only_admin(
    id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency)
):
    await UserService.delete_user(user_id=id, session=session)



