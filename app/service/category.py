import logging
from typing import Optional
from sqlalchemy import asc
from sqlalchemy.orm import Session
from app.dto.core.category import CategoryDTO, GetListCategoryResponse
from app.model.category import Category

from setting import setting

_logger = logging.getLogger(__name__)

DATA_PATH = setting.DATA_STORAGE

class CategoryService:    
    @classmethod
    def get_list_category(cls, db: Session):
        categories = Category.q(db, Category.deleted_at.is_(None)) \
                    .order_by(asc(Category.id)) \
                    .all()
        list_categories = []
        for category in categories:
            category = CategoryDTO(**category.to_dict())
            list_categories.append(category)
        return GetListCategoryResponse(categories=list_categories)
