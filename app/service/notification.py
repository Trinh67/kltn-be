import logging
from typing import Optional
from sqlalchemy import and_, desc
from app.model import Notification
from sqlalchemy.orm import Session
from app.dto.core.auth import UserDTO
from app.dto.core.notification import GetListNotificationResponse, NotificationItemResponse

from setting import setting

_logger = logging.getLogger(__name__)

class NotificationService:
    @classmethod
    def get_list_notification(cls, db: Session, user: UserDTO):
        notifications = Notification.q(db, and_(Notification.user_id == user.user_id, Notification.deleted_at.is_(None), Notification.is_read == 0)) \
                    .order_by(desc(Notification.id)) \
                    .limit(8)
        list_notifications = []
        for notification in notifications:
            notification = NotificationItemResponse(**notification.to_dict())
            list_notifications.append(notification)
        return GetListNotificationResponse(notifications=list_notifications)

    @classmethod
    def make_all_read(cls, db: Session, user: UserDTO):
        db.query(Notification).filter(Notification.user_id == user.user_id).update({"is_read": 1})
        db.commit()

        return None
