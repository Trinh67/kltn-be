from datetime import datetime
from typing import List, Optional, Union
from unicodedata import category

from pydantic import Field, root_validator
from app.dto.base import CamelBaseModel
from app.dto.core.pagination import PaginationResponse
from app.helper.enum import FileStatus, ActionFile


class FileDTO(CamelBaseModel):
    class Config:
        orm_mode = True

    id: int
    file_title: str
    file_name: str
    category_id: int
    file_description: str
    pages: int
    views: int
    downloads: int
    updated_at: Union[int, datetime]
    type: Optional[str]
    google_driver_id: Optional[str]
    status: FileStatus
    refuse_reason: Optional[str]

    @root_validator()
    def validate_duration(cls, values):
        if values.get('file_name'):
            values['type'] = values.get('file_name').split('.')[1]

        return values


class GetFileDBResponse(FileDTO):
    author_name: Optional[str]
    file_path: str
    category_vi: str
    category_en: str


class GetListFileResponse(PaginationResponse):
    files: List[GetFileDBResponse]


class GetListCategoryFileResponse(PaginationResponse):
    files: List[GetFileDBResponse]


class SearchFileMappingResponse(PaginationResponse):
    files: List[GetFileDBResponse]


class UploadFileResponse(CamelBaseModel):
    file_name: str = Field(alias="fileName")


class UpdateStatusFileRequest(CamelBaseModel):
    id: int
    type: FileStatus
    google_driver_id: Optional[str]
    refuse_reason: Optional[str]


class UpdateStatusFileResponse(CamelBaseModel):
    file_id: int


class ActionFileRequest(CamelBaseModel):
    id: int
    type: ActionFile
    share_to_user_id: Optional[List[str]]


class ActionFileResponse(CamelBaseModel):
    file_id: int


class SharedListRequest(CamelBaseModel):
    file_id: int


class SharedListResponse(CamelBaseModel):
    emails: List[str]


class FileStatistic(CamelBaseModel):
    total: int
    status: int

class StatisticFileResponse(CamelBaseModel):
    files: List[FileStatistic]