from sqlalchemy import UUID, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.data.models import Base


class Floor(Base):
    """Этаж."""

    __tablename__ = "floors"

    number = Column(Integer, nullable=False)
    section_id = Column(UUID, ForeignKey("sections.id"))
    section = relationship("Section", back_populates="floors")

    properties = relationship("Property", back_populates="floor")
