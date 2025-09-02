from pydantic import BaseModel
from typing import Optional
from .brand import Brand
from .category import Category

class ProductBase(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float

class ProductCreate(ProductBase):
    brand_id: int
    category_id: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None

class Product(ProductBase):
    brand: Brand
    category: Category

    class Config:
        orm_mode = True
