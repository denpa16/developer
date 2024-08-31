from fastapi import APIRouter, Path
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.models import Project, Property
from app.dependencies.resourses import async_session

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/")
async def list_projects(session: AsyncSession = async_session):
    """Список проектов."""
    subquery_max_price = (
        select(
            Property.project_id,
            func.max(Property.price).label("max_price"),
        )
        .group_by(Property.project_id)
        .subquery()
    )
    result = await session.execute(
        select(
            Project,
            func.coalesce(subquery_max_price.c.max_price, 0).label("max_price"),
        ).outerjoin(subquery_max_price, subquery_max_price.c.project_id == Project.id),
    )
    return result.scalars().all()


@router.get("/{alias}")
async def retrieve_project(
    alias: str = Path(description="", alias="alias"),
    session: AsyncSession = async_session,
):
    """Получение проекта."""
    result = await session.execute(select(Project).where(Project.alias == alias))
    return result.scalars().one()
