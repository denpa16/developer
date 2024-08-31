from app.common.paginations import LimitOffsetPagination


class ProjectLimitOffsetPagination(LimitOffsetPagination):
    """Пагинация для проектов."""

    limit = 10
