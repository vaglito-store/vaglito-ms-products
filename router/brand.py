from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from settings.database import get_db
from models.brand import Brand
from schemas import brand

router = APIRouter(
    prefix="/brands",
    tags=["Brands"]
)

# Get all brands
@router.get("/", response_model=List[brand.Brand])
def get_brands(db: Session = Depends(get_db)):
    brands = db.query(Brand).all()
    return brands

# Get brand by ID
@router.get("/{brand_id}", response_model=brand.Brand)
def get_product(brand_id: int, db: Session = Depends(get_db)):
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(
            status_code=404,
            detail="Brand not found"
        )
    return brand

# Create Brand
@router.post("/", response_model=brand.Brand, status_code=status.HTTP_201_CREATED)
def create_brand(brand: brand.BrandCreate, db: Session = Depends(get_db)):
    existing_brand = db.query(Brand).filter_by(name=brand.name).first()
    if existing_brand:
        raise HTTPException(
            status_code=400,
            detail=f"Brand '{brand.name}' already exists"
        )
    new_brand = Brand(**brand.dict())
    db.add(new_brand)
    db.commit()
    db.refresh(new_brand)
    return new_brand

# Update Brand
@router.put("/{brand_id}", response_model=brand.Brand)
def update_brand(brand_id: int, update_brand: brand.Brand, db: Session = Depends(get_db)):
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(
            status_code=404,
            detail="Brand not found"
        )

    for key, value in update_brand.dict().items():
        setattr(brand, key, value)

    db.commit()
    db.refresh(brand)
    return brand

# Delete Brand
@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(
            status_code=404,
            detail="Brand not found"
        )
    db.delete(brand)
    db.commit()
    return {
        "message": "Brand deleted sucessfully"
    }


