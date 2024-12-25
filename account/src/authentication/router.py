from fastapi import APIRouter, Form, HTTPException, Request, status, Depends
from fastapi.security import HTTPBearer

from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import ErrorResponseModel
from src.authentication.schemas import CredentialsJSON, CredentialsForm, TokenInfo
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
    print(await request.json())
    print(request.headers.get('content-type'))
    content_type = request.headers.get('content-type')
    if content_type == 'applocation/json':
        credentials = await request.json()
        credentials_model = CredentialsJSON(**credentials)
    elif content_type == 'applocation/x-www-form-urlencoded':
        form = await request.form()
        credentials_model = CredentialsForm(username=form["username"], password=form["password"])
    else:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported media type"
        )
    return await AuthService.sign_in(credentials_model.username, credentials_model.password, session)