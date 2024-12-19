from app.common.filters import FacetFilterSet, CharFilter, CharInFilter, RelationshipFilter, IntegerInFilter
from app.data.models import Project


class ProjectFilter(FacetFilterSet):
    """Фильтр для проектов."""

    alias = CharInFilter()
    buildings = IntegerInFilter(field_name="buildings")
    buildings.facets_skip = True
    buildings.specs_skip = True

    class Meta:
        model = Project
