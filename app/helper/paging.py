from pydantic import BaseModel
from typing import Generic, Sequence, Type, TypeVar
from pydantic.generics import GenericModel
from contextvars import ContextVar


T = TypeVar("T")
C = TypeVar("C")


class Pagination(BaseModel):
    current_page: int
    page_size: int
    total_items: int


class Page(GenericModel, Generic[T]):
    items: Sequence[T]
    pagination: Pagination

    @classmethod
    def create(cls, items: Sequence[T], pagination: Pagination) -> "Page[T]":
        return cls(
            items=items,
            pagination=pagination
        )


PageType: ContextVar[Type[Page]] = ContextVar("PageType", default=Page)


class KeysetPagination(BaseModel):
    offset: int = 0
    limit: int = 20


class KeysetPage(GenericModel, Generic[T]):
    items: Sequence[T]
    pagination: KeysetPagination

    @classmethod
    def create(cls, items: Sequence[T], pagination: KeysetPagination) -> "KeysetPage[T]":
        return cls(
            items=items,
            pagination=pagination
        )


KeysetPageType: ContextVar[Type[KeysetPage]] = ContextVar("KeysetPageType", default=KeysetPage)

