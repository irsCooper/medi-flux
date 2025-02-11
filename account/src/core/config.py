import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent.parent

load_dotenv()

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certificates" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certificates" / "jwt-publick.pem"
    algorithms: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30 

class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()
    echo: bool = True 
    db_url: str = os.environ.get('DB_URL')
    rabbit_mq_url: str = os.environ.get('RMQ_URL')



settings = Settings()