from core.database.settings.base import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    product_name = Column(String, unique=True)
    description = Column(String, nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    price = Column(Float)
    currency = Column(String, default="JOD", nullable=False)
    image = Column(String, nullable=False)
    product_creator = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=func.now())
    deleted_at = Column(DateTime, default=None)

    user = relationship("User", back_populates="products")
    category = relationship("Category", back_populates="products")


class Favourite(Base):
    __tablename__ = "favourites"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    user = relationship("User")
    product = relationship("Product")
