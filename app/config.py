from urllib.parse import quote
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Docker Credentials
    DOCKER_POSTGRES_USER: str
    DOCKER_POSTGRES_PASSWORD: str
    DOCKER_POSTGRES_DB: str
    DOCKER_POSTGRES_PORT: str = "5432"

    # Local Credentials
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str

    JWT_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str

    ENV: str = "development"

    @property
    def DATABASE_URL(self) -> str:
        if self.ENV == "docker":
            quoted_pass = quote(self.DOCKER_POSTGRES_PASSWORD)
            return f"postgresql+psycopg2://{self.DOCKER_POSTGRES_USER}:{quoted_pass}@db:{self.DOCKER_POSTGRES_PORT}/{self.DOCKER_POSTGRES_DB}"
        else:
            quoted_pass = quote(self.POSTGRES_PASSWORD)
            return f"postgresql+psycopg2://{self.POSTGRES_USER}:{quoted_pass}@localhost:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"
        from_attributes = True


settings = Settings()
