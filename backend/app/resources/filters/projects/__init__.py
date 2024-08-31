import contextlib

from fastapi import Request

from .project_filter import ProjectFilter

__all__ = ("ProjectFilter",)


async def get_filter_class(request: Request) -> ProjectFilter:
    """Получение класса фильтра."""
    filter_class = ProjectFilter(request)
    with contextlib.suppress(Exception):
        yield filter_class
