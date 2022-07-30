from sqlalchemy import Column, Integer, String, Text

from app.model.base import BareBaseModel
from sqlalchemy.orm import relationship


class File(BareBaseModel):
    __tablename__ = 'file'

    user_id = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=False)
    file_name = Column(String(255), nullable=True)
    file_description = Column(Text(255), nullable=True)
    pages = Column(Integer, nullable=False, default=0)
    views = Column(Integer, nullable=False, default=0)
    downloads = Column(Integer, nullable=False, default=0)
    file_elastic_id = Column(Text(255), nullable=True)
    file_title = Column(Text(255), nullable=True)

    #relationship
    users = relationship("User", foreign_keys='File.user_id',
                         primaryjoin='and_(File.user_id == User.user_id, User.deleted_at.is_(None))',
                         back_populates="files",
                         uselist=False, lazy='select')
    categories = relationship("Category", foreign_keys='File.category_id',
                         primaryjoin='and_(File.category_id == Category.id, Category.deleted_at.is_(None))',
                         back_populates="files",
                         uselist=False, lazy='select')
