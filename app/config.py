# app/config.py — Application Configuration & Settings
import os
from pydantic import BaseModel

class Settings(BaseModel):
    title: str = "DART AI Studio"
    version: str = "1.0.0"
    environment: str = os.getenv("ENVIRONMENT", "development")
    port: int = int(os.getenv("PORT", "8000"))
    allowed_origins: list[str] = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    db_url: str = os.getenv("DATABASE_URL", "sqlite:///dart.db")

settings = Settings()
