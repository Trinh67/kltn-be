import os
from typing import List
from pyparsing import Optional
from app.dto.base import CamelBaseModel

from pydantic import root_validator, validator, Field
from app.helper.constant import Constant

from app.helper.custom_exception import InvalidFileFormat


class UploadFileResponse(CamelBaseModel):
    file_name: str = Field(alias="fileName")


class CreateFileResponse(CamelBaseModel):
    id: str


class GetFileResponse(CamelBaseModel):
    id: str
    content: str


class CreateFileRequest(CamelBaseModel):
    file_path: str
    user_id: int

    @validator('file_path')
    def validate_file_path(cls, value):
        name, ext = os.path.splitext(value)
        if ext not in Constant.SUPPORTED_FILE_EXT:
            raise InvalidFileFormat

        return value


class SearchFileResponse(CamelBaseModel):
    total: int
    files: List[str]


class SearchFileRequest(CamelBaseModel):
    content: str
    size: int = Field(default=5)