from fastapi import APIRouter
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.models import Property
from app.data.sqlalchemy_session import async_session

router = APIRouter(prefix="/properties", tags=["Properties"])


@router.get("/")
async def get_list(session: AsyncSession = async_session):
    """Список этажй."""
    result = await session.execute(select(Property))
    return result.scalars().all()


@router.get("/bulk_create")
async def bulk_create(session: AsyncSession = async_session):
    """Создание этажи."""
    result = await session.execute(select(Property))
    return result.scalars().all()


@router.get("/delete_all")
async def delete_all(session: AsyncSession = async_session):
    """Удалить все этажи."""
    await session.execute(delete(Property))
    result = await session.execute(select(Property))
    return result.scalars().all()
