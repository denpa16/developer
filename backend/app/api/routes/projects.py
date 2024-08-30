import secrets

from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.models import Project
from app.data.sqlalchemy_session import async_session

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/")
async def get_list() -> list:
    """Список проектов."""
    return []


@router.get("/")
async def get_retrieve() -> dict:
    """Проект."""
    return {}


@router.get("/create_one")
async def create(session: AsyncSession = async_session) -> list:
    """Создание проекта."""
    session.add(
        Project(name=f"name_{secrets.randbelow(1000)}", alias=f"alias_{secrets.randbelow(1000)}"),
    )
    result = await session.execute(select(Project))
    return result.scalars().all()
