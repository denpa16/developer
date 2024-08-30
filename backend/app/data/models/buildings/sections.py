from sqlalchemy import UUID, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.data.models import Base


class Section(Base):
    """Секция."""

    __tablename__ = "sections"

    number = Column(Integer, nullable=False)
    building_id = Column(UUID, ForeignKey("buildings.id"))
    building = relationship("Building", back_populates="sections")

    floors = relationship("Floor", back_populates="section")
    properties = relationship("Property", back_populates="section")
