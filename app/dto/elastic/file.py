
from typing import List
from pydantic import Field

from app.dto.base import CamelBaseModel


class GetFileResponse(CamelBaseModel):
    id: str
    content: str


class CreateFileResponse(CamelBaseModel):
    id: str


class SearchFileResponse(CamelBaseModel):
    total: int
    files: List[str]
