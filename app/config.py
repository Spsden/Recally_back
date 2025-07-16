from pydantic import BaseSettings

class Settings(BaseSettings):
    REDIS_URL: str = "redis://localhost:6379/0"
    DATABASE_URL: str = "sqlite:///./recally.db"

    # Cloudflare R2 Settings
    CLOUDFLARE_R2_ACCOUNT_ID: str
    CLOUDFLARE_R2_ACCESS_KEY_ID: str
    CLOUDFLARE_R2_SECRET_ACCESS_KEY: str
    CLOUDFLARE_R2_BUCKET_NAME: str
    CLOUDFLARE_R2_PUBLIC_URL: str # e.g., https://pub-YOUR_UUID.r2.dev/your-bucket-name

    class Config:
        env_file = ".env"

settings = Settings()
