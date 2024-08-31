from __future__ import annotations

from pydantic import RedisDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    """Настройки Redis."""

    scheme: str = "scheme"
    port: int = 6379
    host: str = "localhost"
    dsn: RedisDsn | None | str = None
    expire: int = 60 * 60 * 120

    @field_validator("dsn", mode="before")
    @classmethod
    def dsn_build(cls: RedisSettings, value: str | None, values: ValidationInfo) -> str:
        """Создание dsn для Redis."""
        if isinstance(value, str):
            return value
        return RedisDsn.build(
            scheme=values.data.get("scheme"),
            host=values.data.get("host"),
            port=values.data.get("port"),
        ).unicode_string()

    class Config:
        """Конфиги."""

        env_prefix = "redis_"
