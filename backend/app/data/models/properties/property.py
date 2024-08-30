from sqlalchemy import UUID, Column, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship

from app.data.models import Base


class Property(Base):
    """Объекты собственности."""

    __tablename__ = "properties"

    project_id = Column(UUID, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="properties")
    building_id = Column(UUID, ForeignKey("buildings.id"))
    building = relationship("Building", back_populates="properties")
    section_id = Column(UUID, ForeignKey("sections.id"))
    section = relationship("Section", back_populates="properties")
    floor_id = Column(UUID, ForeignKey("floors.id"))
    floor = relationship("Floor", back_populates="properties")
    number = Column(Integer, nullable=False)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
