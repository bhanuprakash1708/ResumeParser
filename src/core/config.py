# Location: /src/core/config.py
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings
    """
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "myuser")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "mypassword")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "resume_parser_db")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")

    DATABASE_URL_OVERRIDE: str = os.getenv("DATABASE_URL", "sqlite:///./resume_parser.db")

    # Construct the database URL
    @property
    def DATABASE_URL(self) -> str:
        if self.DATABASE_URL_OVERRIDE and self.DATABASE_URL_OVERRIDE.strip():
            return self.DATABASE_URL_OVERRIDE.strip()
        return "sqlite:///./resume_parser.db"

    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")


# Create a single instance of the settings to be imported by other files
settings = Settings()
