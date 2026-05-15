from enum import StrEnum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # App
    APP_NAME: str = "PDF Merger API"
    ENV: Environment = Environment.DEVELOPMENT
    RATE_LIMIT: str = "5/minute"
    CORS_ALLOWED_ORIGINS: str = ""

    @property
    def DEBUG(self) -> bool:
        return self.ENV == Environment.DEVELOPMENT


settings = Settings()
