from sqlalchemy.orm import Session
from app import models
from app.schemas.category import CategoryBase, CategoryCreate, CategoryOut


class CategoryService:
    def __init__(self, db: Session):
        self.db = db

    def create_category(self, user_id: int, category_in: CategoryCreate):
        existing = (self.db.query(models.Category).filter(
            models.Category.name == category_in.name, models.Category.user_id == user_id
        ).first())

        if existing:
            return None

        new_category = models.Category(name=category_in.name, user_id=user_id)

        self.db.add(new_category)
        self.db.commit()
        self.db.refresh(new_category)
        return new_category

    def list_categories(self, user_id: int):
        return self.db.query(models.Category).filter(models.Category.user_id == user_id).all()

    def get_category(self, user_id: int, category_id: int):
        return (self.db.query(models.Category).filter(
            models.Category.user_id == user_id, models.Category.id == category_id
        ).first()
        )

    def delete_category(self, user_id: int, category_id: int):
        category = self.get_category(user_id, category_id)

        if not category:
            return None

        self.db.delete(category)
        self.db.commit()

        return category
