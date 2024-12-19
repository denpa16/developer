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
        self._query = None
        self.request = request
        self.query_params = dict(self.request.query_params)
        self.session = kwargs.get("session")

    async def __call__(self: FilterSet, *args, **kwargs):
        self._query = kwargs.get("query")
        return await self._filter_query()

    class Meta:
        model = None

    async def _filter(self):
        return await self._filter_query()

    async def _filter_query(self):
        _filters = await self._get_filters()
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
    async def _filter_list(cls):
        return cls.__dict__.keys()

    async def _get_filters(self):
        filters = {}
        attrs = await self._filter_list()
        for key in attrs:
            attr = getattr(self, key)
            if isinstance(attr, BaseFilter | BaseInFilter):
                filters[key] = attr
        return filters

class FacetFilterSet(FilterSet):
    """FacetFilterset."""

    async def _get_facet_choices(self, field_name, result):
        choices = []
        for item in result:
            if attr := getattr(item[0], field_name):
                choices.append(attr)
        return choices

    async def facets(self, *_: tuple, **kwargs: dict):
        self._query = kwargs.get("query")
        _session = kwargs.get("session")
        _filtered_query = await self._filter_query()
        result = await _session.execute(_filtered_query)
        _result = result.fetchall()
        _facets = []
        _count = len(_result)
        _filters = await self._get_filters()
        for filter_name, _filter in _filters.items():
            name = _filter.field_name if _filter.field_name else filter_name
            _filter_facets_skip = (
                _filter.facets_skip if hasattr(_filter, "facets_skip") else False
            )
            if _filter_facets_skip:
                continue
            if hasattr(_filter, "facets"):
                method = _filter.facets
                _facets.append(
                    {"name": filter_name, "choices": getattr(self, method)(_session)}
                )
                continue
            _facets.append(
                {
                    "name": name,
                    "choices": await self._get_facet_choices(name, result),
                }
            )
        return {"facets": _facets, "count": _count}