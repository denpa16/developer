from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship

from app.data.models import Base


class Project(Base):
    """Проект."""

    __tablename__ = "projects"

    name = Column(String, nullable=False)
    alias = Column(String, nullable=False)

    city_id = Column(UUID, ForeignKey("cities.id"))
    city = relationship("City", back_populates="projects")

    buildings = relationship("Building", back_populates="project")
    properties = relationship("Property", back_populates="project")
