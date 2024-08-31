import contextlib

from fastapi import APIRouter, Depends, Path, Request
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.models import Project, Property
from app.dependencies.resourses import async_session

router = APIRouter(prefix="/projects", tags=["Projects"])


class ProjectLimitOffsetPagination:
    """Пагинация для списка проектов."""

    offset = 0
    limit = 10

    def __init__(self: "ProjectLimitOffsetPagination", request: Request) -> None:
        """Инициализация."""
        self.request = request
        self.query_params = dict(self.request.query_params)
        self.offset = (
            int(self.query_params.get("offset")) if self.query_params.get("offset") else self.offset
        )
        self.limit = (
            int(self.query_params.get("limit")) if self.query_params.get("limit") else self.limit
        )

    def __call__(self: "ProjectLimitOffsetPagination", *_: tuple, **kwargs: dict) -> list:
        """Вызов."""
        self.results = kwargs.get("results") if kwargs.get("results") else []
        return self.__paginate_result()

    def __paginate_result(self: "ProjectLimitOffsetPagination") -> list:
        """Пагианция."""
        if self.results:
            return self.results[self.offset : self.offset + self.limit]
        return []


async def get_pagination_class(request: Request):
    """Получение класса пагиации."""
    pagination_class = ProjectLimitOffsetPagination(request)
    with contextlib.suppress(Exception):
        yield pagination_class


paginator_class: ProjectLimitOffsetPagination = Depends(get_pagination_class)


@router.get("/")
async def list_projects(
    session: AsyncSession = async_session,
    pagination: ProjectLimitOffsetPagination = paginator_class,
):
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
    return pagination(results=result.scalars().all())


@router.get("/{alias}")
async def retrieve_project(
    alias: str = Path(description="", alias="alias"),
    session: AsyncSession = async_session,
):
    """Получение проекта."""
    result = await session.execute(select(Project).where(Project.alias == alias))
    return result.scalars().one()
