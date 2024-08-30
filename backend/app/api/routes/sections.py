from fastapi import APIRouter
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.models import Building, Section
from app.data.sqlalchemy_session import async_session

router = APIRouter(prefix="/sections", tags=["Sections"])


@router.get("/")
async def get_list(session: AsyncSession = async_session):
    """Список секций."""
    result = await session.execute(select(Section))
    return result.scalars().all()


@router.get("/bulk_create")
async def bulk_create(session: AsyncSession = async_session):
    """Создание секции."""
    buildings_query = await session.execute(select(Building))
    buildings = buildings_query.scalars().all()
    count = 15
    sections = [
        Section(
            number=i + 1,
            building_id=building.id,
        )
        for i in range(count)
        for building in buildings
    ]
    session.add_all(sections)
    result = await session.execute(select(Section))
    return result.scalars().all()


@router.get("/delete_all")
async def delete_all(session: AsyncSession = async_session):
    """Удалить все секции."""
    await session.execute(delete(Section))
    result = await session.execute(select(Section))
    return result.scalars().all()
