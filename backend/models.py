from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MyProduct(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    current_price: float
    stock: int
    category: str
    image: Optional[str] = None

class CompetitorData(BaseModel):
    id: Optional[str] = Field(alias="_id")
    product_name: str
    competitor_name: str
    price: float
    discount: Optional[float] = 0.0
    last_updated: Optional[datetime] = None
