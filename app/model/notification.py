from sqlalchemy import Column, Integer, String

from app.model.base import BareBaseModel
from sqlalchemy.orm import relationship


class Notification(BareBaseModel):
    __tablename__ = 'notification'

    user_id = Column(String(50), nullable=False)
    is_read = Column(Integer, nullable=False, default=0)
    content = Column(String(255), nullable=False)

    #relationship
    users = relationship("User", foreign_keys='Notification.user_id',
                         primaryjoin='and_(Notification.user_id == User.user_id, User.deleted_at.is_(None))',
                         back_populates="notifications",
                         uselist=False, lazy='select')
