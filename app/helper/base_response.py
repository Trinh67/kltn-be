from typing import TypeVar, Generic, Sequence, Optional, Union

from pydantic import BaseModel
from pydantic.generics import GenericModel

from app.dto.core.pagination import PaginationResponse
from app.helper.paging import Pagination, KeysetPagination
from starlette_context import context
from app.util.common import parse_accept_language

T = TypeVar("T")


class ResponseSchemaBase(BaseModel):
    __abstract__ = True

    code: int = ""
    message: str = ""

    def custom_response(self, code: int, message: str):
        try:
            lang = parse_accept_language(context.data.get('lang'))
        except:
            lang = "vi"

        self.code = code
        message_translated = getattr(message, lang, message)
        self.message = message_translated
        return self

    def success_response(self):
        self.code = 200
        self.message = 'Success'
        return self

    def fail_response(self, code: int, message: str):
        self.code = code
        self.message = message
        return self


class DataResponse(ResponseSchemaBase, GenericModel, Generic[T]):
    data: Optional[T] = None

    class Config:
        arbitrary_types_allowed = True

    def custom_response(self, code: int, message: str, data: T):
        self.code = code
        self.message = message
        self.data = data
        return self

    def success_response(self, data: Optional[T]):
        self.code = 200
        self.message = 'Success'
        self.data = data
        return self

    def fail_response(self, code: int, message: str, data: T = None):
        self.code = code
        self.message = message
        self.data = data
        return self


class PagingDataResponse(ResponseSchemaBase, GenericModel, Generic[T]):
    data: Optional[T] = None

    def success_response(self, data: PaginationResponse, pagination: Union[Pagination, KeysetPagination]):
        self.code = 200
        self.message = "Success"
        self.data = data
        self.data.pagination = pagination
        return self