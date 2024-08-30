from sqlalchemy import UUID, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.data.models import Base


class Building(Base):
    """Корпус."""

    __tablename__ = "buildings"

    number = Column(Integer, nullable=False)
    project_id = Column(UUID, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="buildings")

    sections = relationship("Section", back_populates="building")
    properties = relationship("Property", back_populates="building")
