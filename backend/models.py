# models.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class SignupModel(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"

class LoginModel(BaseModel):
    username: str
    password: str

class ProductInDB(BaseModel):
    name: str
    current_price: Optional[float] = None
    category: Optional[str] = None
    image: Optional[str] = None
    weight: Optional[float] = None
    price_history: Optional[List[Dict]] = Field(default_factory=list)
    competitor_data: Optional[List[Dict]] = Field(default_factory=list)
