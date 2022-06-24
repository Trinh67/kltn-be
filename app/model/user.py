from sqlalchemy import Column, String

from app.model.base import BareBaseModel


class User(BareBaseModel):
    __tablename__ = 'user'

    name = Column(String(50), nullable=False)
