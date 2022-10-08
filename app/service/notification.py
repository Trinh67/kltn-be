import logging
from typing import Optional
from sqlalchemy import and_, asc
from app.model import Notification
from sqlalchemy.orm import Session
from app.dto.core.auth import UserDTO
from app.dto.core.notification import NotificationDTO, GetListNotificationResponse

from setting import setting

_logger = logging.getLogger(__name__)

DATA_PATH = setting.DATA_STORAGE

class NotificationService:    
    @classmethod
    def get_list_notification(cls, db: Session, user: UserDTO):
        notifications = Notification.q(db, and_(Notification.user_id == user.user_id, Notification.deleted_at.is_(None))) \
                    .order_by(asc(Notification.id)) \
                    .limit(5)
        list_notifications = []
        for notification in notifications:
            notification = NotificationDTO(**notification.to_dict())
            list_notifications.append(notification)
        return GetListNotificationResponse(categories=list_notifications)
