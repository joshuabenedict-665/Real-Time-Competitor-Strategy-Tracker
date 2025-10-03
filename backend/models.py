from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class MyProduct(Base):
    __tablename__ = "my_products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    current_price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    image = Column(String, nullable=True)

class CompetitorData(Base):
    __tablename__ = "competitor_data"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    competitor_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
