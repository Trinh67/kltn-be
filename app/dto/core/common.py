import logging
import typing
from pathlib import Path
from typing import Type, Any, Union

from fastapi import UploadFile as UploadFileSource
from pydantic import BaseModel, Field
from starlette.datastructures import UploadFile as StarletteUploadFile

from app.dto.base import CamelBaseModel
from app.helper.exception_handler import Message, ValidateException

_logger = logging.getLogger(__name__)


class UploadFileRequest(UploadFileSource):
    file: typing.IO
    filename: str
    file_data = Union[bytes, str]

    @classmethod
    def validate(cls: Type['UploadFileRequest'], v: Any) -> Any:
        if not isinstance(v, StarletteUploadFile) or not v.file or not v.filename:
            raise ValidateException(402, Message(en = 'Param file is required', \
                                                 vi = 'Tệp bắt buộc nhập'))
        path = Path(v.filename)
        if not path.name or path.suffix.lower() not in ['.jpg', '.png', 'svg', '.csv', '.xls', '.xlsx', '.pdf', '.txt',
                                                        '.docs', '.doc', '.docx', '.pptx']:
            raise ValidateException(415, Message(en = 'File type is not supported', \
                                                 vi = 'Định dạng tệp tải lên không được hỗ trợ'))
        return v


class DownloadFileRequest(CamelBaseModel):
    file_path: str
