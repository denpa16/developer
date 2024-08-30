from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings

DATABASE_URL = settings.database.dsn


class AsyncSessionBuilder:
    """Строитель асинхронной сессии."""

    def __init__(self: "AsyncSessionBuilder", database_url: str, echo: bool = False) -> None:
        """Инициалиазция."""
        self.database_url = database_url
        self.engine = create_async_engine(database_url, echo=echo)

    def __call__(self: "AsyncSessionBuilder", *_: tuple, **__: dict) -> async_sessionmaker:
        """Вызов."""
        self.session = async_sessionmaker(self.engine, expire_on_commit=False)
        return self.session


session_builder = AsyncSessionBuilder(database_url=DATABASE_URL, echo=settings.database.echo)


async def get_db_session() -> AsyncSession:
    """Получение сессии с БД."""
    async_session: async_sessionmaker = session_builder()
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()

        await session.commit()


async_session: AsyncSession = Depends(get_db_session)
