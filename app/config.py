from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    REDIS_URL: str = "redis://localhost:6379/0"
    # The DATABASE_URL should be set in the .env file
    # Example for PostgreSQL: postgresql://user:password@host:port/dbname
    DATABASE_URL: str = "postgresql://recally:recally@db:5432/recally"

    # Cloudinary Settings
    # The pydantic settings automatically maps .env files
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    class Config:
        env_file = ".env"

settings = Settings()