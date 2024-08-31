from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.models import Project
from app.data.sqlalchemy_session import async_session

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/")
async def get_projects_list(session: AsyncSession = async_session):
    """Список проектов."""
    result = await session.execute(select(Project))
    return result.scalars().all()
