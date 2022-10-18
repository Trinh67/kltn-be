from typing import List, Union
from datetime import datetime

from sqlalchemy import alias
from app.dto.base import CamelBaseModel


class NotificationDTO(CamelBaseModel):
    class Config:
        orm_mode = True

    id: int
    content: str
    created_at: Union[int, datetime]

class NotificationItemResponse(NotificationDTO):
    pass


class GetListNotificationResponse(CamelBaseModel):
    notifications: List[NotificationDTO]