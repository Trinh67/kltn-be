from sqlalchemy import Column, Integer, String

from app.model.base import BareBaseModel
from sqlalchemy.orm import relationship


class Favorite(BareBaseModel):
    __tablename__ = 'favorite'

    user_id = Column(String(50), nullable=False)
    file_id = Column(Integer, nullable=False)

    #relationship
    users = relationship("User", foreign_keys='Favorite.user_id',
                         primaryjoin='and_(Favorite.user_id == User.user_id, User.deleted_at.is_(None))',
                         back_populates="favorites",
                         uselist=False, lazy='select')
    files = relationship("File", foreign_keys='Favorite.file_id',
                         primaryjoin='and_(Favorite.file_id == File.id, File.deleted_at.is_(None))',
                         back_populates="favorites",
                         uselist=False, lazy='select')
