from urllib.parse import quote
from pydantic import computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str

    JWT_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str

    ENV: str = "development"

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        quoted_pass = quote(self.POSTGRES_PASSWORD)
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{quoted_pass}@db:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"  # allows extra fields without error
        from_attributes = True  # replaces old orm_mode


settings = Settings()
