"""Application configuration via pydantic-settings.

Every environment variable the service consumes lives here, typed.
Other modules import the ``settings`` instance — never read
``os.environ`` directly.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Strongly-typed application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "myapi"
    app_version: str = "0.0.1"
    debug: bool = False

    secret_key: str = Field(default="change-me", description="Replace before deploy.")
    database_url: str = Field(
        default="sqlite:///./local.db",
        description="SQLAlchemy URL. Override per environment.",
    )

    cors_origins: list[str] = Field(default_factory=list)


@lru_cache
def get_settings() -> Settings:
    """Cached accessor — useful for FastAPI dependency overrides in tests."""
    return Settings()


settings = get_settings()
