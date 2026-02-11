from pydantic import BaseSettings, Field
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "taskify"
    ENV: str = "development"
    DEBUG: bool = True

    SECRET_KEY: str = Field("change_me_super_secret", env="SECRET_KEY", repr=False)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    DATABASE_URL: Optional[str] = Field(None, env="DATABASE_URL", repr=False)
    REDIS_URL: Optional[str] = Field(None, env="REDIS_URL", repr=False)
    CELERY_BACKEND: Optional[str] = Field(None, env="CELERY_BACKEND", repr=False)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
