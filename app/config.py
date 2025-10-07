import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database configurations
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # App settings
    JWT_KEY: str = os.getenv("JWT_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    ALGORITHM: str = os.getenv("ALGORITHM")

    # Optional: environment flag
    ENV: str = os.getenv("ENV", "development")


settings = Settings()
