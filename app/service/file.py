import logging
from sqlalchemy.orm import Session
from app.adapter.elastic import ElasticService
from app.dto.core.file import GetFileResponse, GetListFileResponse
from app.model.file import File

from setting import setting

_logger = logging.getLogger(__name__)

DATA_PATH = setting.DATA_STORAGE

class FileService:    
    @classmethod
    def get_file(cls, db: Session, id: str):
        file = File.q(db, File.id == id).first()
        return GetFileResponse(**file.to_dict())
    
    @classmethod
    def get_list_file(cls, db: Session, user_id: int):
        files = File.q(db, File.user_id == user_id).all()
        dto_files = []
        for file in files:
            dto_file = GetFileResponse(**file.to_dict())
            dto_files.append(dto_file)
        
        return GetListFileResponse(files=dto_files)
