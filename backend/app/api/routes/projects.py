from uuid import UUID

from fastapi import APIRouter, Path
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.models import Project
from app.data.sqlalchemy_session import async_session

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/")
async def get_list(session: AsyncSession = async_session):
    """Список проектов."""
    result = await session.execute(select(Project))
    return result.scalars().all()


@router.get("/{id}")
async def get_retrieve(id: UUID = Path(alias="id"), session: AsyncSession = async_session):
    """Получить проект."""
    result = await session.execute(select(Project).where(Project.id == id))
    return result.scalars().one()


@router.get("/bulk_create")
async def bulk_create(session: AsyncSession = async_session):
    """Создание проекта."""
    count = 15
    projects = [
        Project(
            name=f"Project_{i + 1}",
            alias=f"Alias_{i + 1}",
        )
        for i in range(count)
    ]
    session.add_all(projects)
    result = await session.execute(select(Project))
    return result.scalars().all()


@router.get("/delete_all")
async def delete_all(session: AsyncSession = async_session):
    """Удалить все проекты."""
    await session.execute(delete(Project))
    result = await session.execute(select(Project))
    return result.scalars().all()
