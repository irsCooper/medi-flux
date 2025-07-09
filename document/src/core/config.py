import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings


ROLE_ADMIN = 'Admin'
ROLE_USER = 'User'
ROLE_DOCTOR = 'Doctr'
ROLE_MANAGER = 'Manager'


BASE_DIR = Path(__file__).parent.parent.parent

ENVIRONMENT = os.getenv("ENV", "dev")
load_dotenv(f".env.{ENVIRONMENT}")



class AuthJWT(BaseModel):
    public_key_path: Path = BASE_DIR / "certificates" / "jwt-publick.pem"
    algorithms: str = "RS256"


class Settings(BaseSettings):
    echo: bool = os.environ.get('ECHO')
    db_url: str = os.environ.get('DB_URL')
    es_url: str = os.environ.get('ES_URL')
    rabbit_mq_url: str = os.environ.get('RMQ_URL')
    auth_jwt: AuthJWT = AuthJWT()

    class Config:
        env_file = f".env.{ENVIRONMENT}"

settings: Settings = Settings()
