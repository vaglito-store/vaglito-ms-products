from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from settings.database import get_db
from models.product import Product
from models.brand import Brand
from models.category import Category
from schemas import product

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# Get all products
@router.get("/", response_model=List[product.Product])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

# Get product by ID
@router.get("/{product_id}", response_model=product.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    return product

# Create Product
@router.post("/", response_model=product.ProductCreate, status_code=status.HTTP_201_CREATED)
def create_product(product: product.ProductCreate, db: Session = Depends(get_db)):
    db_brand = db.query(Brand).filter(Brand.id == product.brand_id).first()
    db_category = db.query(Category).filter(Category.id == product.category_id).first()

    if not db_brand:
        raise HTTPException(
            status_code=404,
            detail="Brand not found"
        )
    if not db_category:
        raise HTTPException(
            status_code=404,
            detail="Brand not found"
        )

    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# Update Product
@router.put("/{product_id}", response_model=product.Product)
def update_product(product_id: int, update_product: product.Product, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    for key, value in update_product.dict().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

# Delete product
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()
    return {
        "message": "Product deleted sucessfully"
    }
