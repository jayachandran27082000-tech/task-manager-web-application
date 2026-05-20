from pydantic_settings import BaseSettings
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "taskmanager.db")


class Settings(BaseSettings):
    SECRET_KEY: str = "fallback-dev-secret-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DATABASE_URL: str = f"sqlite:///{DB_PATH}"

    class Config:
        env_file = ".env"


settings = Settings()