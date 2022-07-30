

from typing import List, Optional
from app.dto.base import CamelBaseModel


class CategoryDTO(CamelBaseModel):
    class Config:
        orm_mode = True

    id: int
    name_vi: str
    name_en: str
    parent_id: Optional[int]


class GetListCategoryResponse(CamelBaseModel):
    categories: List[CategoryDTO]