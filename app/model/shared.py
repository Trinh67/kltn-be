from sqlalchemy import Column, Integer, String

from app.model.base import BareBaseModel
from sqlalchemy.orm import relationship


class Shared(BareBaseModel):
    __tablename__ = 'shared'

    from_user_id = Column(String(50), nullable=False)
    to_user_id = Column(String(50), nullable=False)
    file_id = Column(Integer, nullable=False)

    #relationship
    users = relationship("User", foreign_keys='Shared.to_user_id',
                         primaryjoin='and_(Shared.to_user_id == User.user_id, User.deleted_at.is_(None))',
                         back_populates="shareds",
                         uselist=False, lazy='select')
    files = relationship("File", foreign_keys='Shared.file_id',
                         primaryjoin='and_(Shared.file_id == File.id, File.deleted_at.is_(None), Shared.from_user_id == File.user_id)',
                         back_populates="shareds",
                         uselist=False, lazy='select')
