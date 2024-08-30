from pydantic_settings import BaseSettings

from .settings import (
    AppSettings,
    DatabaseSettings,
)


class Settings(BaseSettings):
    """Настройки."""

    database: DatabaseSettings = DatabaseSettings()
    app: AppSettings = AppSettings()


settings = Settings()
