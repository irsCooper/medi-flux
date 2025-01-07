from fastapi import APIRouter, HTTPException, Request, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.accounts.model import UserModel
from src.exceptions import ErrorResponseModel
from src.authentication.schemas import CredentialsJSON, CredentialsForm, TokenInfo
from src.authentication.service import AuthService
from src.core.db_helper import db
from src.accounts.schemas import UserCreate
from src.dependencies import get_current_auth_access, http_bearer


router = APIRouter(
    prefix="/Authentication",
    tags=["Authentication"],
    dependencies=[Depends(http_bearer)]
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


@router.post("/SignIn", openapi_extra={
    'requestBody': {
        'content': {
            'applocation/json': {
                'schema': CredentialsJSON.model_json_schema()
            },
            'application/x-www-form-urlencoded': {
                'schema': CredentialsForm.model_json_schema()
            }
        },
        'required': True
    },
    'responses': {
        401: {
            'description': 'Invalid credentials',
            'content': {
                'application/json': {
                    'schema': ErrorResponseModel.model_json_schema(),
                    'example': {
                        'detail': "Invalid username or password"
                    }
                }
            }
        }
    }
})
async def sign_in(
    request: Request,
    session: AsyncSession = Depends(db.session_dependency)
) -> TokenInfo:
    content_type = request.headers.get('content-type')
    if content_type == 'applocation/json':
        credentials = await request.json()
        credentials_model = CredentialsJSON(**credentials)
    elif content_type == 'application/x-www-form-urlencoded':
        form = await request.form()
        credentials_model = CredentialsForm(username=form["username"], password=form["password"])
    else:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported media type"
        )
    return await AuthService.sign_in(credentials_model.username, credentials_model.password, session)


@router.put("/SingOut", status_code=status.HTTP_200_OK)
async def sign_out(
    user: UserModel = Depends(get_current_auth_access),
    session: AsyncSession = Depends(db.session_dependency)
):
    return await AuthService.sing_out(user.id, session)


@router.get("/Validate", status_code=status.HTTP_200_OK)
async def validate_token(access_token: str):
    token = await AuthService.validate_access_token(access_token)
    if token: 
        return token
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalit token"
    )


@router.post("/Refresh", status_code=status.HTTP_200_OK, response_model=TokenInfo)
async def refresh_token(
    refresh_token: str,
    session: AsyncSession = Depends(db.session_dependency)
):
    return await AuthService.refresh_tokens(refresh_token, session)