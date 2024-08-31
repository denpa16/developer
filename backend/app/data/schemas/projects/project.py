from pydantic import UUID4, BaseModel


class ProjectList(BaseModel):
    """Schema для проектов."""

    id: UUID4
    alias: str
    name: str
