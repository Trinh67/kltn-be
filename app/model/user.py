from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.model.base import BareBaseModel


class User(BareBaseModel):
    __tablename__ = 'user'

    name = Column(String(50), nullable=False)
    user_id = Column(String(50), nullable=False)

    # relationship
    files = relationship("File", lazy='select', foreign_keys='File.user_id',
                        primaryjoin='and_(File.user_id == User.user_id, File.deleted_at.is_(None))', back_populates="users")
