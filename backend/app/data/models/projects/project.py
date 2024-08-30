from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.data.models import Base


class Project(Base):
    """Проект."""

    __tablename__ = "projects"

    name = Column(String, nullable=False)
    alias = Column(String, nullable=True)

    buildings = relationship("Building", back_populates="project")
    properties = relationship("Property", back_populates="project")
