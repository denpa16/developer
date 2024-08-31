from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import Request


class FilterSet:
    """Filterset."""

    def __init__(self: FilterSet, request: Request) -> None:
        """Инициализация."""
        self.request = request
        self.query_params = dict(self.request.query_params)

    def __call__(self: FilterSet, *_: tuple, **kwargs: dict) -> dict:
        """Вызов."""
