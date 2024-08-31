from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.sqlalchemy_session import get_db_session
from app.resources.filters.projects import ProjectFilter, get_filter_class
from app.resources.paginations.projects import ProjectLimitOffsetPagination, get_pagination_class

async_session: AsyncSession = Depends(get_db_session)
projects_paginator_class: ProjectLimitOffsetPagination = Depends(get_pagination_class)
projects_filter_class: ProjectFilter = Depends(get_filter_class)
