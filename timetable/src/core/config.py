import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    echo: bool = True
    db_url: str = os.environ.get('DB_URL')

settings = Settings()
