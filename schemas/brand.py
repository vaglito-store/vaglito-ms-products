from pydantic import BaseModel, Field

class BrandBase(BaseModel):
    id: int
    name: str

class BrandCreate(BaseModel):
    name: str = Field(..., description="Brand name (required)")

class Brand(BrandBase):

    class Config:
        orm_mode = True
