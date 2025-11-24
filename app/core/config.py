import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Gym Management API"
    API_V1_STR: str = "/api/v1"
    # IMPORTANT: Set a strong secret in your environment (e.g., Render dashboard)
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    # CORS origins for the frontend. Use a list of allowed origins in production.
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # Database settings
    # Set DATABASE_URL in your environment for production (e.g., Render PostgreSQL)
    DATABASE_URL: str

    # Allow extra environment variables
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore",
    }

settings = Settings()