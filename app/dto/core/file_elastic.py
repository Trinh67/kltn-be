import os
from typing import List, Optional
from app.dto.base import CamelBaseModel

from pydantic import validator, Field
from app.helper.constant import Constant

from app.helper.custom_exception import InvalidFileFormat


class CreateFileResponse(CamelBaseModel):
    id: str


class GetFileResponse(CamelBaseModel):
    id: str
    content: str


class ElasticPagination(CamelBaseModel):
    total: int
    size: int


class GetListFileResponse(CamelBaseModel):
    files: List[GetFileResponse]
    pagination: ElasticPagination


class CreateFileRequest(CamelBaseModel):
    file_path: str
    file_title: str
    file_description: str
    category_id: int

    @validator('file_path')
    def validate_file_path(cls, value):
        name, ext = os.path.splitext(value)
        if ext not in Constant.SUPPORTED_FILE_EXT:
            raise InvalidFileFormat

        return value


class CreateFileResponse(CamelBaseModel):
    new_file_id: int


class SearchFileResponse(CamelBaseModel):
    total: int
    files: List[str]


class SearchFileRequest(CamelBaseModel):
    content: str
    size: int = Field(default=5)