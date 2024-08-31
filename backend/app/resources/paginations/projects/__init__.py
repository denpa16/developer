import contextlib

from fastapi import Request

from .project_limit_offset_pagination import ProjectLimitOffsetPagination

__all__ = ("ProjectLimitOffsetPagination",)


async def get_pagination_class(request: Request) -> ProjectLimitOffsetPagination:
    """Получение класса пагиации."""
    pagination_class = ProjectLimitOffsetPagination(request)
    with contextlib.suppress(Exception):
        yield pagination_class
