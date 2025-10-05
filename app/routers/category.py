from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import category as schemas
from app.services.category_service import CategoryService
from app.deps import get_db, get_current_user

router = APIRouter(prefix="/categories", tags=["categories"])

# -------------------------------
# Create Category
# -------------------------------


@router.post("/", response_model=schemas.CategoryOut)
def create_category(category_in: schemas.CategoryCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service = CategoryService(db)
    category = service.create_category(current_user.id, category_in)

    if not category:
        raise HTTPException(status_code=400, detail="Category already exists")

    return category

# -------------------------------
# List All Categories
# -------------------------------


@router.get("/", response_model=List[schemas.CategoryOut])
def list_categories(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service = CategoryService(db)
    return service.list_categories(current_user.id)

# -------------------------------
# Get Category
# -------------------------------


@router.get("/{category_id}", response_model=schemas.CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service = CategoryService(db)
    category = service.get_category(current_user.id, category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category

# -------------------------------
# Delete Category
# -------------------------------


@router.delete("/{category_id}", response_model=schemas.CategoryOut)
def delete_category(category_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service = CategoryService(db)
    deleted = service.delete_category(current_user.id, category_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")

    return deleted
