from fastapi import APIRouter, Form, HTTPException, status, Depends
from fastapi.security import HTTPBearer

from sqlalchemy.ext.asyncio import AsyncSession

from src.accounts.service import UserService
from src.core.db_helper import db
from src.accounts.schemas import UserCreate, UserCreateAdmin


router = APIRouter(
    prefix="/Authentication",
    tags=["Authentication"],
)


@router.post("/SignUp", status_code=status.HTTP_201_CREATED)
async def sign_up(
    user_create: UserCreate,
    session: AsyncSession = Depends(db.session_dependency),
):
    await UserService.create_user(user_in=user_create, session=session)
    return {
        "status_code": status.HTTP_201_CREATED,
        "detail": "User created",
    }

