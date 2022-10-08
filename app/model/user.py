from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.model.base import BareBaseModel


class User(BareBaseModel):
    __tablename__ = 'user'

    name = Column(String(50), nullable=False)
    user_id = Column(String(50), nullable=False)
    email = Column(String(255), nullable=True)
    avatar_url = Column(String(255), nullable=False)
    source = Column(String(50), nullable=True)

    # relationship
    files = relationship("File", lazy='select', foreign_keys='File.user_id',
                        primaryjoin='and_(User.user_id == File.user_id, File.deleted_at.is_(None))', back_populates="users")
    
    favorites = relationship("Favorite", foreign_keys='Favorite.user_id',
                        primaryjoin='and_(User.user_id == Favorite.user_id, Favorite.deleted_at.is_(None))', back_populates="users")
    
    shareds = relationship("Shared", foreign_keys='Shared.to_user_id',
                        primaryjoin='and_(User.user_id == Shared.to_user_id, Shared.deleted_at.is_(None))', back_populates="users")
    
    notifications = relationship("Notification", foreign_keys='Notification.user_id',
                        primaryjoin='and_(User.user_id == Notification.user_id, Notification.deleted_at.is_(None))', back_populates="users")