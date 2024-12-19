from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select


from app.common.filters.filter import BaseFilter, BaseInFilter, RelationshipFilter

if TYPE_CHECKING:
    from fastapi import Request


class FilterSet:
    """Filterset."""

    def __init__(self: FilterSet, request: Request, *_: tuple, **kwargs: dict) -> None:
        """Инициализация."""
        self.request = request
        self.query_params = dict(self.request.query_params)
        self.session = kwargs.get("session")

    async def __call__(self: FilterSet, *args, **kwargs):
        self._query = kwargs.get("query")
        return await self.__filter_query()

    class Meta:
        model = None

    async def __filter(self):
        return await self.__filter_query()

    async def __filter_query(self):
        _filters = await self.get_filters()
        for query_key, value in self.query_params.items():
            if _filter := _filters.get(query_key):
                key = (
                    _filter.field_name
                    if (
                        _filter.field_name
                    )
                    else query_key
                )
                if _filter.method:
                    try:
                        self._query = getattr(self, _filter.method)(self._query, query_key, value)
                    except AttributeError:
                        raise AttributeError
                if isinstance(_filter, BaseFilter):
                    model_field = getattr(self.Meta.model, key)
                    self._query = self._query.where(
                        getattr(model_field, _filter.lookup_expr)(value)
                    )
                if isinstance(_filter, BaseInFilter):
                    model_field = getattr(self.Meta.model, key)
                    self._query = self._query.where(
                        getattr(model_field, _filter.lookup_expr)(value.split(","))
                    )
                if isinstance(_filter, RelationshipFilter):
                    if _filter.field_name is None:
                        continue
                    relationship = getattr(self.Meta.model, query_key)
                    self._query = self._query.where(
                        relationship.any(**{_filter.field_name: value})
                    )
        return self._query

    @classmethod
    async def filter_list(cls):
        return cls.__dict__.keys()

    async def get_filters(self):
        filters = {}
        attrs = await self.filter_list()
        for key in attrs:
            attr = getattr(self, key)
            if isinstance(attr, BaseFilter | BaseInFilter):
                filters[key] = attr
        return filters

class FacetFilterSet(FilterSet):
    """FacetFilterset."""

    async def facets(self):
        return {"facets": [], "count": 0}