import logging
from typing import Optional
from fastapi import APIRouter, Depends, File, Form
from sqlalchemy.orm import Session
from app.dto.core.auth import UserDTO
from app.dto.core.common import UploadFileRequest
from app.dto.core.file import GetFileDBResponse, GetListCategoryFileResponse, GetListFileResponse, SharedListRequest, SharedListResponse, StatisticFileResponse, UpdateStatusFileRequest, UpdateStatusFileResponse, \
     UploadFileResponse, ActionFileRequest, ActionFileResponse
from app.helper.base_response import DataResponse, PagingDataResponse
from app.helper.db import db_session
from app.helper.enum import FileStatus
from app.helper.middleware import get_current_user
from app.service import common_service
from app.service.file import FileService



router = APIRouter()

_logger = logging.getLogger(__name__)


@router.post('/upload-file', response_model=DataResponse[UploadFileResponse])
def upload_document_file(*, upload_file_request: UploadFileRequest = File(...), user: Optional[UserDTO] = Depends(get_current_user)):
    data = common_service.upload_file(user_id=user.user_id ,file=upload_file_request)
    return DataResponse().success_response(data=data)


@router.get('/', response_model=DataResponse[GetFileDBResponse])
def get_file(db: Session = Depends(db_session),
                                  *, id: int):
    data = FileService.get_file(db, id=id)
    return DataResponse().success_response(data=data)


@router.get('/category', response_model=DataResponse[GetListCategoryFileResponse])
def get_category_file(db: Session = Depends(db_session),
                                  *, id: int):
    data, pagination = FileService.get_category_file(db, id=id)
    return PagingDataResponse().success_response(data=data, pagination=pagination)


@router.get('/list-file', response_model=PagingDataResponse[GetListFileResponse])
def get_list_file(db: Session = Depends(db_session),
                                  *, user_id: Optional[int] = None):
    data, pagination = FileService.get_list_file(db, user_id=user_id)
    return PagingDataResponse().success_response(data=data, pagination=pagination)


@router.get('/filter-file', response_model=PagingDataResponse[GetListFileResponse])
def filter_file(db: Session = Depends(db_session),
                                  *, type: Optional[FileStatus] = None, user: Optional[UserDTO] = Depends(get_current_user)):
    data, pagination = FileService.filter_file(db, user=user, type=type)
    return PagingDataResponse().success_response(data=data, pagination=pagination)


@router.post('/update-status-file', response_model=DataResponse[UpdateStatusFileResponse])
def update_status_file(db: Session = Depends(db_session), *, update_status_file_request: UpdateStatusFileRequest, user: Optional[UserDTO] = Depends(get_current_user)):
    data = FileService.update_status_file(db, user=user, request=update_status_file_request)
    return DataResponse().success_response(data=data)


@router.post('/action-file', response_model=DataResponse[ActionFileResponse])
def action_file(db: Session = Depends(db_session), *, action_file_request: ActionFileRequest, user: Optional[UserDTO] = Depends(get_current_user)):
    data = FileService.action_file(db, user=user, request=action_file_request)
    return DataResponse().success_response(data=data)


@router.post('/shared-list', response_model=DataResponse[SharedListResponse])
def get_shared_list(db: Session = Depends(db_session), *, shared_list_request: SharedListRequest, user: Optional[UserDTO] = Depends(get_current_user)):
    data = FileService.get_shared_list(db, request=shared_list_request, user=user)
    return DataResponse().success_response(data=data)


@router.get('/statistic', response_model=DataResponse[StatisticFileResponse])
def get_statistic_file(db: Session = Depends(db_session), user: UserDTO = Depends(get_current_user)):
    data = FileService.get_statistic_file(db, user)
    return DataResponse().success_response(data=data)