from pydantic import BaseModel
from typing import Optional
from .brand import Brand
from .category import Category

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    brand_id: int
    category_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    brand: Brand
    category: Category

    class Config:
        orm_mode = True
