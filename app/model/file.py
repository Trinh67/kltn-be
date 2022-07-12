from email.policy import default
from sqlalchemy import Column, Integer, String, Text

from app.model.base import BareBaseModel


class File(BareBaseModel):
    __tablename__ = 'file'

    user_id = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=False)
    file_name = Column(String(255), nullable=True)
    file_description = Column(Text(255), nullable=True)
    views = Column(Integer, nullable=True, default=0)
    downloads = Column(Integer, nullable=True, default=0)
    file_elastic_id = Column(Text(255), nullable=True)
