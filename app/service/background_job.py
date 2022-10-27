import logging

from sqlalchemy import and_, desc, or_
from sqlalchemy.orm import Session
from app.helper.enum import FileStatus

from app.model.file import File
from setting import setting

_logger = logging.getLogger(__name__)

class BackgroundJobService:
    @classmethod
    def upload_file_to_elastic_search(cls, db: Session):
        _logger.info('Stating job upload file to Elastic')
        list_file = File.q(db, File.status == FileStatus.PROCESSING, File.deleted_at.is_(None))
        list_id = [file.id for file in list_file]
        print(list_id)
        _logger.info(f'Start up load {len(list_id)} files')
        _logger.info('Finish job upload file to Elastic')
        
        return
