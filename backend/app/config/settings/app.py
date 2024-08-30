from os import getenv

from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Настройки приложения."""

    title: str = getenv("TITLE", "fastapi_template")
    secret_key: str = getenv("SECRET_KEY", "my_very_secret_key")

    class Config:
        """Конфиг."""

        env_prefix = "app_"
