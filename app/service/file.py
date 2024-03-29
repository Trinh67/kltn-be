from datetime import datetime
import logging
from typing import Optional
from sqlalchemy import and_, desc, func
from sqlalchemy.orm import Session
from app.dto.core.auth import UserDTO
from app.dto.core.file import FileStatistic, GetFileDBResponse, GetListCategoryFileResponse, GetListFileResponse, SharedListRequest, SharedListResponse, StatisticFileResponse, UpdateStatusFileRequest, UpdateStatusFileResponse, ActionFileRequest
from app.helper.custom_exception import InvalidField, ObjectNotFound, PermissionDenied
from app.helper.enum import ActionFile, FileStatus
from app.helper.paging import Pagination
from app.model import Shared, Favorite, File, User
from app.model.notification import Notification

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
    def get_category_file(cls, db: Session, id: Optional[int]):
        files = File.q(db, File.deleted_at.is_(None), File.status == FileStatus.APPROVED.value) \
                    .join(File.users) \
                    .filter(File.category_id == id) \
                    .order_by(desc(File.id)) \
                    .all()

        total_files = len(files)
        dto_files = []
        for file in files:
            file_path = f"{file.user_id}/{file.file_name}"
            dto_file = GetFileDBResponse(**file.to_dict(), file_path=file_path, author_name=file.users.name, \
                                         category_vi=file.categories.name_vi, category_en=file.categories.name_en)
            dto_files.append(dto_file)
        
        return GetListCategoryFileResponse(files=dto_files), Pagination(total_items=total_files, current_page=1, page_size=100)
    
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
                            .join(Favorite,
                                and_(Favorite.deleted_at.is_(None),
                                    Favorite.user_id == user.user_id,
                                    Favorite.file_id == File.id)) \
                            .order_by(desc(File.id)).all()
            if type == FileStatus.SHARED:
                files = db.query(File) \
                            .filter(and_(File.deleted_at.is_(None), File.status == FileStatus.APPROVED.value)) \
                            .join(File.users) \
                            .join(Shared,
                                and_(Shared.deleted_at.is_(None),
                                    Shared.to_user_id == user.user_id,
                                    Shared.file_id == File.id,
                                )) \
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
        if request.type != FileStatus.DELETE.value and user.email != 'trinhxuantrinh.yd267@gmail.com':
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
                    # create notification
                    new_notification = {
                        'user_id': file.user_id,
                        'is_read': 0,
                        'content': f'File "{file.file_title}" has Approved by Admin!'
                    }
                    Notification.create(db, new_notification)
                else:
                    db.query(File) \
                        .filter(File.id == request.id) \
                        .update({"status": request.type.value, "refuse_reason": request.refuse_reason})
                    # create notification
                    new_notification = {
                        'user_id': file.user_id,
                        'is_read': 0,
                        'content': f'File "{file.file_title}" has Refuse by Admin!'
                    }
                    Notification.create(db, new_notification)
            db.commit()
            return UpdateStatusFileResponse(file_id = request.id)
        except Exception as e:
            _logger.exception(e)
    
    @classmethod
    def action_file(cls, db: Session, request: ActionFileRequest, user: UserDTO):
        file = File.q(db, and_(File.id == request.id, File.deleted_at.is_(None))).first()
        if not file:
            raise ObjectNotFound("File")
        if file.status not in [FileStatus.APPROVED.value]:
            raise InvalidField("Id")
        
        try:
            if request.type == ActionFile.REMOVELIKED.value:
                db.query(Favorite) \
                    .filter(and_(Favorite.file_id == request.id, Favorite.user_id == user.user_id)) \
                    .update({"deleted_at": datetime.now()})
            if request.type == ActionFile.REMOVESHARED.value:
                if file.user_id != user.user_id:
                    raise ObjectNotFound("File")
                db.query(Shared) \
                    .filter(and_(Shared.file_id == request.id, Shared.from_user_id == user.user_id, Shared.to_user_id == request.share_to_user_id)) \
                    .update({"deleted_at": datetime.now()})
            if request.type == ActionFile.LIKED.value:
                favorite_dict = {
                    "user_id": user.user_id,
                    "file_id": request.id
                }
                Favorite.create(db, favorite_dict)
                # create notification
                new_notification = {
                    'user_id': file.user_id,
                    'is_read': 0,
                    'content': f'File "{file.file_title}" has Liked by {user.email}!'
                }
                Notification.create(db, new_notification)
            if request.type == ActionFile.SHARED.value:
                if str(file.user_id) != str(user.user_id):
                    raise ObjectNotFound("File")
                for to_user_id in request.share_to_user_id:
                    share_dict = {
                        "from_user_id": user.user_id,
                        "to_user_id": to_user_id,
                        "file_id": request.id
                    }
                    Shared.create(db, share_dict)
                    # create notification
                    new_notification = {
                        'user_id': to_user_id,
                        'is_read': 0,
                        'content': f'File "{file.file_title}" has Shared to you by {user.email}!'
                    }
                    Notification.create(db, new_notification)
            db.commit()
            return UpdateStatusFileResponse(file_id = request.id)
        except Exception as e:
            _logger.exception(e)
    
    @classmethod
    def get_shared_list(cls, db: Session, request: SharedListRequest, user: UserDTO):
        emails = db.query(User) \
                    .join(Shared,
                        and_(Shared.deleted_at.is_(None),
                            Shared.to_user_id == User.user_id),
                        isouter=True
                    ) \
                    .filter(
                        Shared.file_id == request.file_id,
                        Shared.from_user_id == user.user_id) \
                    .order_by(desc(User.id)).distinct().all()
        list_emails = []
        for email in emails:
            list_emails.append(email.email)
        return SharedListResponse(emails=list_emails)
    
    @classmethod
    def get_statistic_file(cls, db: Session, user: UserDTO):
        files = db.query(File.status, func.count(File.id).label('total')). \
            filter(File.deleted_at.is_(None), File.user_id == user.user_id). \
            group_by(File.status).all()
        files_liked = db.query(func.count(File.id).label('total')) \
            .join(Favorite, Favorite.file_id == File.id) \
            .filter(Favorite.deleted_at.is_(None),
                    Favorite.user_id == user.user_id).all()
        files_shared = db.query(func.count(File.id).label('total')) \
            .join(Shared, Shared.file_id == File.id) \
            .filter(Shared.deleted_at.is_(None),
                    Shared.to_user_id == user.user_id).all()
        list_file = []
        for file in files:
            list_file.append(FileStatistic.parse_obj(file))

        list_file.append(FileStatistic.parse_obj({"status": 5, "total": files_liked[0].total}))
        list_file.append(FileStatistic.parse_obj({"status": 6, "total": files_shared[0].total}))

        return StatisticFileResponse(files=list_file)
