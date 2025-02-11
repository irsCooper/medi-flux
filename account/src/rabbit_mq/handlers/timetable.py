from src.authentication.service import AuthService
from fastapi.exceptions import HTTPException

async def check_token_handler(token: str) -> bytes:
    try:
        await AuthService.validate_access_token(token=token)
        return b'\x01'
    except HTTPException as e:
        return str(e.detail).encode()