import os
from enum import StrEnum
from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # App
    app_name: str = "PDF Merger API"
    env: Environment = Environment.DEVELOPMENT
    rate_limit: str = "5/minute"
    cors_allowed_origins: list[str] = []

    @property
    def debug(self) -> bool:
        return self.env == Environment.DEVELOPMENT

    @model_validator(mode="after")
    def validate_production_config(self) -> "Settings":
        required = ["CORS_ALLOWED_ORIGINS", "ENV", "RATE_LIMIT"]
        missing = [key for key in required if not os.environ.get(key)]

        if missing:
            raise RuntimeError(
                f"Missing required environment variables: {', '.join(missing)}. "
                "Check your .env file or environment configuration."
            )

        return self


@lru_cache()
def get_settings() -> Settings:
    """
    Returns cached settings instance.
    Using lru_cache ensures settings are loaded once.
    """
    return Settings()
