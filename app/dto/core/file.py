import os
from pyparsing import Optional
from app.dto.base import CamelBaseModel

from pydantic import root_validator, validator, Field
from app.helper.constant import Constant

from app.helper.custom_exception import InvalidFileFormat


class CreateUploadFileResponse(CamelBaseModel):
    file_name: str = Field(alias="fileName")


class CreateCustomerSetViaMinioRequest(CamelBaseModel):
    file_path: str
    user_id: int

    @validator('file_path')
    def validate_file_path(cls, value):
        name, ext = os.path.splitext(value)
        if ext not in Constant.SUPPORTED_EXCEL_FILE_EXT:
            raise InvalidFileFormat

        return value