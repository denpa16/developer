from app.common.filters import FacetFilterSet, CharFilter, CharInFilter, RelationshipFilter, IntegerInFilter
from app.data.models import Project


class ProjectFilter(FacetFilterSet):
    """Фильтр для проектов."""

    alias = CharInFilter()
    buildings = IntegerInFilter(field_name="building")

    class Meta:
        model = Project
