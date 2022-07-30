from sqlalchemy import Column, Integer, String

from app.model.base import BareBaseModel
from sqlalchemy.orm import relationship


class Category(BareBaseModel):
    __tablename__ = 'category'

    name_vi = Column(String(255), nullable=False)
    name_en = Column(String(255), nullable=False)
    parent_id = Column(Integer, nullable=True)

    #relationship
    files = relationship("File", foreign_keys='File.category_id',
                         primaryjoin='and_(File.category_id == Category.id, File.deleted_at.is_(None))',
                         back_populates="categories",
                         uselist=False, lazy='select')
