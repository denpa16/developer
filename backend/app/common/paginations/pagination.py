from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import Request


class LimitOffsetPagination:
    """Пагинация."""

    offset = 0
    limit = 10

    def __init__(self: LimitOffsetPagination, request: Request) -> None:
        """Инициализация."""
        self.request = request
        self.query_params = dict(self.request.query_params)
        self.offset = (
            int(self.query_params.get("offset")) if self.query_params.get("offset") else self.offset
        )
        self.limit = (
            int(self.query_params.get("limit")) if self.query_params.get("limit") else self.limit
        )

    def __call__(self: LimitOffsetPagination, *_: tuple, **kwargs: dict) -> dict:
        """Вызов."""
        self.results = kwargs.get("results") if kwargs.get("results") else []
        return {
            "count": self.__get_count(),
            "next": self.__get_next(),
            "previous": self.__get_previous(),
            "results": self.__paginate_result(),
        }

    def __paginate_result(self: LimitOffsetPagination) -> list:
        """Пагианция."""
        if self.results:
            return self.results[self.offset : self.offset + self.limit]
        return []

    def __get_count(self: LimitOffsetPagination) -> int:
        """Получение количества."""
        return len(self.results)

    def __get_next(self: LimitOffsetPagination) -> str | None:
        base_url = self.request.url.replace_query_params()
        if self.__get_count() <= self.offset + self.limit:
            return None
        return f"{base_url}?limit={self.limit}&offset={self.offset + self.limit}"

    def __get_previous(self: LimitOffsetPagination) -> str | None:
        base_url = self.request.url.replace_query_params()
        if self.offset - self.limit < 0:
            return None
        return f"{base_url}?limit={self.limit}&offset={self.offset - self.limit}"
