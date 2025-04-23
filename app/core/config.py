# app/core/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_PREFIX: str = "/api"
    PROJECT_NAME: str = "Document Processing Service"
    GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY", "AIzaSyAgdqtYqX7Dx-Hx-xdo2RlOqLB5_x9bEEI")
    GEMINI_MODEL: str = "gemini-1.5-flash"
    GEMINI_MODEL_2: str = "gemini-2.0-flash"
    LOGS_DIR: str = "logs"

    class Config:
        env_file = ".env"

settings = Settings()