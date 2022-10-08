from sqlalchemy import Column, Integer, String

from app.model.base import BareBaseModel
from sqlalchemy.orm import relationship


class File(BareBaseModel):
    __tablename__ = 'file'

    user_id = Column(String(50), nullable=False)
    category_id = Column(Integer, nullable=False)
    file_name = Column(String(255), nullable=True)
    file_description = Column(String(255), nullable=True)
    pages = Column(Integer, nullable=False, default=0)
    views = Column(Integer, nullable=False, default=0)
    downloads = Column(Integer, nullable=False, default=0)
    file_elastic_id = Column(String(255), nullable=True)
    file_title = Column(String(255), nullable=True)
    google_driver_id = Column(String(50), nullable=True)
    status = Column(Integer, nullable=False, default=0)
    refuse_reason = Column(String(255), nullable=True)

    #relationship
    users = relationship("User", foreign_keys='File.user_id',
                         primaryjoin='and_(File.user_id == User.user_id, User.deleted_at.is_(None))',
                         back_populates="files",
                         uselist=False, lazy='select')
    categories = relationship("Category", foreign_keys='File.category_id',
                         primaryjoin='and_(File.category_id == Category.id, Category.deleted_at.is_(None))',
                         back_populates="files",
                         uselist=False, lazy='select')
    favorites = relationship("Favorite", foreign_keys='Favorite.file_id',
                         primaryjoin='and_(Favorite.file_id == File.id, Favorite.deleted_at.is_(None))',
                         back_populates="files",
                         uselist=False, lazy='select')
    shareds = relationship("Shared", foreign_keys='Shared.file_id',
                         primaryjoin='and_(Shared.file_id == File.id, Shared.deleted_at.is_(None))',
                         back_populates="files",
                         uselist=False, lazy='select')
