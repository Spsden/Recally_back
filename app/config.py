from pydantic import BaseSettings

class Settings(BaseSettings):
    REDIS_URL: str = "redis://localhost:6379/0"
    DATABASE_URL: str = "sqlite:///./recally.db"

    class Config:
        env_file = ".env"

settings = Settings()
