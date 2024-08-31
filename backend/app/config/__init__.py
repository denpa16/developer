from pydantic_settings import BaseSettings

from .settings import (
    AppSettings,
    DatabaseSettings,
    RedisSettings,
)


class Settings(BaseSettings):
    """Настройки."""

    database: DatabaseSettings = DatabaseSettings()
    app: AppSettings = AppSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
