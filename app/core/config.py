from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str 
    VERSION: str
    MONGO_URI: str
    DATABASE_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    URL_FRONTEND: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ACCESS_TOKEN_EXPIRE_DAYS: int
    DENUE_API_KEY: str
    DENUE_API_URL: str

    class Config:
        env_file = ".env"

settings = Settings()