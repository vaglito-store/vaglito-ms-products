from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from settings.database import Base


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)

    products = relationship("Product", back_populates="brand")
    
