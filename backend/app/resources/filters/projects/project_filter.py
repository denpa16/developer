from app.common.filters import FacetFilterSet, CharFilter, CharInFilter, RelationshipFilter, IntegerInFilter
from app.data.models import Project


class ProjectFilter(FacetFilterSet):
    """Фильтр для проектов."""

    alias = CharInFilter()
    buildings = IntegerInFilter(field_name="buildings")
    buildings.facets_skip = True
    buildings.specs_skip = True

    city = CharInFilter(method="city_filter")
    city.facets_skip = True


    class Meta:
        model = Project


    async def city_filter(self, query, field_name, field_value):
        relationship = getattr(self.Meta.model, field_name)
        return query.where(relationship.has(**{"alias": field_value}))