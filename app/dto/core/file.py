from typing import List
from app.dto.base import CamelBaseModel


class GetFileResponse(CamelBaseModel):
    id: int
    file_name: str
    category_id: int


class GetListFileResponse(CamelBaseModel):
    files: List[GetFileResponse]