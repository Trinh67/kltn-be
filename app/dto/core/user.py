from typing import List, Optional
from app.dto.base import CamelBaseModel


class UserDTO(CamelBaseModel):
    class Config:
        orm_mode = True

    user_id: str
    email: str


class GetListUserResponse(CamelBaseModel):
    users: List[UserDTO]