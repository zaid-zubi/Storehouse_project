from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database.settings.base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer,primary_key=True,autoincrement=True,unique=True)
    name = Column(String,nullable=False,unique=True)

    products = relationship("Product", back_populates="category")
