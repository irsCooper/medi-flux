from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='http://localhost:8081/api/Authentication/SignIn')

# async def validate_token(token: str = Depends(oauth2_scheme)):
