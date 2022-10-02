from typing import Text
from sqlalchemy import Column, Text
from sqlalchemy.orm import relationship

from app.model.base import BareBaseModel


class User(BareBaseModel):
    __tablename__ = 'user'

    name = Column(Text(50), nullable=False)
    user_id = Column(Text(50), nullable=False)
    email = Column(Text(255), nullable=True)
    avatar_url = Column(Text(255), nullable=False)
    source = Column(Text(50), nullable=True)

    # relationship
    files = relationship("File", lazy='select', foreign_keys='File.user_id',
                        primaryjoin='and_(File.user_id == User.user_id, File.deleted_at.is_(None))', back_populates="users")
