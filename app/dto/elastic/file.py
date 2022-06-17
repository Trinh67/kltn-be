
from pydantic import Field


class FileContent:
    content: str


class GetFileResponse:
    id: str = Field(alias='_id')
    source: FileContent = Field(alias='_source')


class CreateFileResponse:
    id: str
