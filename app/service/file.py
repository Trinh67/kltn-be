from datetime import datetime
import logging
from typing import Optional
from requests import request
from sqlalchemy import and_, desc
from sqlalchemy.orm import Session
from app.adapter.elastic import ElasticService
from app.dto.core.auth import UserDTO
from app.dto.core.file import GetFileDBResponse, GetListFileResponse, UpdateStatusFileRequest, UpdateStatusFileResponse
from app.helper.custom_exception import InvalidField, ObjectNotFound, PermissionDenied
from app.helper.enum import FileStatus
from app.helper.paging import Pagination
from app.model.file import File
from app.model.user import User

from setting import setting

_logger = logging.getLogger(__name__)

DATA_PATH = setting.DATA_STORAGE

class FileService:    
    @classmethod
    def get_file(cls, db: Session, id: str):
        file = File.q(db, and_(File.id == id, File.deleted_at.is_(None))).join(File.users).first()
        if not file:
            raise ObjectNotFound("File")
        file_path = f"{file.user_id}/{file.file_name}"
        return GetFileDBResponse(**file.to_dict(), author_name=file.users.name, file_path=file_path, \
                                 category_vi=file.categories.name_vi, category_en=file.categories.name_en)
    
    @classmethod
    def get_list_file(cls, db: Session, user_id: Optional[int]):
        if user_id:
            files = File.q(db, and_(File.user_id == user_id, File.deleted_at.is_(None), File.status == FileStatus.APPROVED.value)) \
                        .join(File.users) \
                        .order_by(desc(File.id)).all()
        else:
            files = File.q(db, File.deleted_at.is_(None), File.status == FileStatus.APPROVED.value) \
                        .join(File.users) \
                        .order_by(desc(File.id)) \
                        .all()

        total_files = len(files)
        dto_files = []
        for file in files:
            file_path = f"{file.user_id}/{file.file_name}"
            dto_file = GetFileDBResponse(**file.to_dict(), file_path=file_path, author_name=file.users.name, \
                                         category_vi=file.categories.name_vi, category_en=file.categories.name_en)
            dto_files.append(dto_file)
        
        return GetListFileResponse(files=dto_files), Pagination(total_items=total_files, current_page=1, page_size=100)

    @classmethod
    def filter_file(cls, db: Session, type: Optional[FileStatus], user: UserDTO):
        if user.email == 'trinhxuantrinh.yd267@gmail.com':
            if type is not None:
                files = File.q(db, and_(File.deleted_at.is_(None), File.status == type.value)) \
                            .join(File.users) \
                            .order_by(desc(File.id)).all()
            else:
                files = File.q(db, and_(File.deleted_at.is_(None))) \
                            .join(File.users) \
                            .order_by(desc(File.id)) \
                            .all()
        elif type is not None:
            if type == FileStatus.UPLOADED:
                files = File.q(db, and_(File.user_id == user.user_id, File.deleted_at.is_(None))) \
                            .join(File.users) \
                            .order_by(desc(File.id)).all()
            if type == FileStatus.LIKED:
                files = File.q(db, and_(File.deleted_at.is_(None), File.status == FileStatus.APPROVED.value)) \
                            .join(File.users) \
                            .join(File.favorites) \
                            .order_by(desc(File.id)).all()
            if type == FileStatus.SHARED:
                files = File.q(db, and_(File.user_id == user.user_id, File.deleted_at.is_(None), File.status == FileStatus.APPROVED.value)) \
                            .join(File.users) \
                            .join(User.shareds) \
                            .order_by(desc(File.id)).all()
        else:
            files = File.q(db, and_(File.deleted_at.is_(None), File.user_id == user.user_id)) \
                        .join(File.users) \
                        .order_by(desc(File.id)) \
                        .all()

        total_files = len(files)
        dto_files = []
        for file in files:
            file_path = f"{file.user_id}/{file.file_name}"
            dto_file = GetFileDBResponse(**file.to_dict(), file_path=file_path, author_name=file.users.name, \
                                         category_vi=file.categories.name_vi, category_en=file.categories.name_en)
            dto_files.append(dto_file)
        
        return GetListFileResponse(files=dto_files), Pagination(total_items=total_files, current_page=1, page_size=100)

    @classmethod
    def update_status_file(cls, db: Session, request: UpdateStatusFileRequest, user: UserDTO):
        if user.email != 'trinhxuantrinh.yd267@gmail.com':
            raise PermissionDenied
        if request.type not in [FileStatus.APPROVED, FileStatus.REFUSE, FileStatus.DELETE]:
            raise InvalidField("type")
        file = File.q(db, and_(File.id == request.id, File.deleted_at.is_(None))).first()
        if not file:
            raise ObjectNotFound("File")
        try:
            if request.type == FileStatus.DELETE:
                db.query(File) \
                    .filter(File.id == request.id) \
                    .update({"deleted_at": datetime.now(), "status": request.type.value})
            else:
                if file.status != FileStatus.DRAFT.value:
                    raise InvalidField("File")
                if request.type == FileStatus.APPROVED:
                    db.query(File) \
                        .filter(File.id == request.id) \
                        .update({"status": request.type.value, "google_driver_id": request.google_driver_id})
                else:
                    db.query(File) \
                        .filter(File.id == request.id) \
                        .update({"status": request.type.value, "refuse_reason": request.refuse_reason})
            db.commit()
            return UpdateStatusFileResponse(file_id = request.id)
        except Exception as e:
            _logger.exception(e)