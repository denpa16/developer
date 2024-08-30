from sqlalchemy import Column, String

from app.data.models import Base


class Project(Base):
    """Проект."""

    __tablename__ = "projects"

    name = Column(String, nullable=False)
    alias = Column(String, nullable=True)
