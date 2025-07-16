from pydantic import BaseSettings

class Settings(BaseSettings):
    REDIS_URL: str = "redis://localhost:6379/0"
    DATABASE_URL: str = "sqlite:///./recally.db"
    FIREBASE_SERVICE_ACCOUNT_KEY_PATH: str = "./firebase_service_account.json"
    FIREBASE_STORAGE_BUCKET: str = "your-firebase-storage-bucket-name.appspot.com"

    class Config:
        env_file = ".env"

settings = Settings()