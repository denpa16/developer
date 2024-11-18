from app.common.filters import FilterSet, CharFilter, CharInFilter, RelationshipFilter, IntegerInFilter
from app.data.models import Project


class ProjectFilter(FilterSet):
    """Фильтр для проектов."""
    alias = CharInFilter()
    buildings = IntegerInFilter(field_name="building")

    class Meta:
        model = Project

