from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, index=True, nullable=False)

    # Relationship: one organization can have many users
    users = relationship("User", back_populates="organization")
