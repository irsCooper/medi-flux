from fastapi import APIRouter, Form, HTTPException, status, Depends
from fastapi.security import HTTPBearer

from sqlalchemy.ext.asyncio import AsyncSession

from src.authentication.schemas import TokenInfo
from src.authentication.service import AuthService
from src.accounts.service import UserService
from src.core.db_helper import db
from src.accounts.schemas import UserCreate, UserCreateAdmin


router = APIRouter(
    prefix="/Authentication",
    tags=["Authentication"],
)


@router.post("/SignUp", response_model=TokenInfo, status_code=status.HTTP_201_CREATED)
async def sign_up(
    user_create: UserCreate,
    session: AsyncSession = Depends(db.session_dependency),
):
    return await AuthService.sign_up(
        user_in=user_create,
        session=session
    )


