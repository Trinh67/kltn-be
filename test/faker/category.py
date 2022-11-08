from sqlalchemy.orm import Session
from app.model.category import Category


class CategoryProvider:
    @classmethod
    def create_category_model(cls, db: Session, commit: bool = False, **data) -> Category:
        category = {
            'id': data.get('id', 1),
            "name_vi": data.get("name_vi", "Đại số"),
            "name_en": data.get("name_en", "Math"),
            "parent_id": data.get("parent_id", None)
        }

        new_category: Category = Category.create(db, category, commit=commit)

        return new_category

