"""Application configuration."""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_prefix="TED_", env_file=".env", extra="ignore")

    environment: str = Field(default="local")
    log_level: str = Field(default="INFO")
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/ted",
        description="SQLAlchemy async database URL.",
    )
    telegram_bot_token: str | None = Field(default=None)
    hermes_base_url: str | None = Field(default=None)
    hermes_api_key: str | None = Field(default=None)


@lru_cache
def get_settings() -> Settings:
    return Settings()
