from fastapi import APIRouter
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.models import Building, Project
from app.data.sqlalchemy_session import async_session

router = APIRouter(prefix="/buildings", tags=["Buildings"])


@router.get("/")
async def get_list(session: AsyncSession = async_session):
    """Список корпусов."""
    result = await session.execute(select(Building))
    return result.scalars().all()


@router.get("/bulk_create")
async def bulk_create(session: AsyncSession = async_session):
    """Создание корпуса."""
    projects_query = await session.execute(select(Project))
    projects = projects_query.scalars().all()
    count = 15
    buildings = [
        Building(
            number=i + 1,
            project_id=project.id,
        )
        for i in range(count)
        for project in projects
    ]
    session.add_all(buildings)
    result = await session.execute(select(Building))
    return result.scalars().all()


@router.get("/delete_all")
async def delete_all(session: AsyncSession = async_session):
    """Удалить все корпусы."""
    await session.execute(delete(Building))
    result = await session.execute(select(Building))
    return result.scalars().all()
