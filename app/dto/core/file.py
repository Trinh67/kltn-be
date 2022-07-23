from datetime import datetime
from typing import List, Optional, Union

from pydantic import Field, root_validator
from app.dto.base import CamelBaseModel
from app.dto.core.pagination import PaginationResponse


class FileDTO(CamelBaseModel):
    class Config:
        orm_mode = True

    id: int
    file_name: str
    category_id: int
    file_description: str
    pages: int
    views: int
    downloads: int
    updated_at: Union[int, datetime]
    type: Optional[str]

    @root_validator()
    def validate_duration(cls, values):
        if values.get('file_name'):
            values['type'] = values.get('file_name').split('.')[1]

        return values


class GetFileDBResponse(FileDTO):
    author_name: Optional[str]


class GetListFileResponse(PaginationResponse):
    files: List[GetFileDBResponse]


class SearchFileMappingResponse(PaginationResponse):
    files: List[GetFileDBResponse]