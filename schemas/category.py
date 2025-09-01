from pydantic import BaseModel, Field

class CategoryBase(BaseModel):
    id: int
    name: str = Field(..., description="Category name (required)")

class CategoryCreate(BaseModel):
    name: str = Field(..., description="Category name (required)")

class Category(CategoryBase):

    class Config:
        orm_mode = True
