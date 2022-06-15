from typing import Optional
from app.dto.base import CamelBaseModel
from pydantic import validator
from app.helper.custom_errors import PageInvalidError, PageSizeInvalidError


class PaginationRequest(CamelBaseModel):
    page: Optional[int] = 1
    page_size: Optional[int] = 10

    @validator('page')
    def validate_page(cls, v):
        if v <= 0:
            raise PageInvalidError

        return v

    @validator('page_size')
    def validate_page_size(cls, v):
        if v <= 0:
            raise PageSizeInvalidError
        return v


class RequiredPaginationRequest(PaginationRequest):
    page: int
    page_size: int


class Pagination(CamelBaseModel):
    current_page: int
    page_size: int
    total_items: int


class PaginationResponse(CamelBaseModel):
    pagination: Optional[Pagination]
