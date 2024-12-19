from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.data.models import Base


class City(Base):
    """Город."""

    __tablename__ = "cities"

    name = Column(String, nullable=False)
    alias = Column(String, nullable=False)

    projects = relationship("Project", back_populates="city")
