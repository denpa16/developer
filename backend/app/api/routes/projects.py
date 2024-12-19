from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Path
from sqlalchemy import func, select

from app.data.models import Project, Property
from app.dependencies.resourses import (
    async_session,
    projects_filter_class,
    projects_paginator_class,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.resources.filters.projects import ProjectFilter
    from app.resources.paginations.projects import ProjectLimitOffsetPagination


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/")
async def list_projects(
    session: AsyncSession = async_session,
    pagination_class: ProjectLimitOffsetPagination = projects_paginator_class,
    filter_class: ProjectFilter = projects_filter_class,
):
    """Список проектов."""

    query = (
        select(
            Project,
        )
    )
    filter_query = await filter_class(query=query)
    result = await session.execute(filter_query)
    return pagination_class(results=result.scalars().all())

@router.get("/facets")
async def facets_projects(
    session: AsyncSession = async_session,
    pagination_class: ProjectLimitOffsetPagination = projects_paginator_class,
    filter_class: ProjectFilter = projects_filter_class,
):
    """Спеки проектов."""

    query = (
        select(
            Project,
        )
    )
    return await filter_class.facets(query=query, session=session)

@router.get("/specs")
async def specs_projects(
    session: AsyncSession = async_session,
    pagination_class: ProjectLimitOffsetPagination = projects_paginator_class,
    filter_class: ProjectFilter = projects_filter_class,
):
    """Спеки проектов."""

    query = (
        select(
            Project,
        )
    )
    return await filter_class.specs(query=query, session=session)


@router.get("/{alias}")
async def retrieve_project(
    alias: str = Path(description="", alias="alias"),
    session: AsyncSession = async_session,
):
    """Получение проекта."""
    result = await session.execute(select(Project).where(Project.alias == alias))
    return result.scalars().one()


@router.get("/{alias}/genplan")
async def project_genplan(
    alias: str = Path(description="", alias="alias"),
    session: AsyncSession = async_session,
):
    """Получение проекта."""
    result = await session.execute(select(Project).where(Project.alias == alias))
    return result.scalars().one()