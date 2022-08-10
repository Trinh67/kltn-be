from __future__ import annotations
from typing import Optional, List

from app.dto.base import CamelBaseModel


class LoginDTO(CamelBaseModel):
    token_id: str


class TokenDTO(CamelBaseModel):
    access_token: Optional[str]
    refresh_token: Optional[str]


class ExchangeAccessTokenDTO(CamelBaseModel):
    refresh_token: str


class UserDTO(CamelBaseModel):
    id: Optional[int]
    name: Optional[str]
    email: Optional[str]
    avatar_url: Optional[str]

    class Config:
        orm_mode = True


class FacebookUserResponse(CamelBaseModel):
    id: Optional[int]
    name: Optional[str]
    email: Optional[str]
    avatar_url: Optional[str]
