from typing import List, Optional
from app.dto.base import CamelBaseModel


class NotificationDTO(CamelBaseModel):
    class Config:
        orm_mode = True

    id: int
    user_id: str
    content: str


class GetListNotificationResponse(CamelBaseModel):
    categories: List[NotificationDTO]