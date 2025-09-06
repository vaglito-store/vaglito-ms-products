from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from settings.database import get_db
from models.category import Category
from schemas import category

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


# Get all categories
@router.get("/", response_model=List[category.Category])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories

# Get category by ID
@router.get("/{category_id}", response_model=category.Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

# Create Category
@router.post("/", response_model=category.Category, status_code=status.HTTP_201_CREATED)
def create_category(category: category.CategoryCreate, db: Session = Depends(get_db)):
    existing_category = db.query(Category).filter_by(name=category.name).first()
    if existing_category:
        raise HTTPException(
            status_code=400,
            detail=f"Category '{category.name}' already exists"
        )
    new_category = Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# Update Category
@router.put("/{category_id}", response_model=category.Category)
def update_category(category_id: int, update_category: category.Category, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    for key, value in update_category.dict().items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return category


# Delete Update
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    db.delete(category)
    db.commit()
    return {
        "message": "Category deleted sucessfully"
    }


        
