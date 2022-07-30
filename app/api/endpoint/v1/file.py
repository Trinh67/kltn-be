import logging
from typing import Optional
from fastapi import APIRouter, Depends, File, Form
from sqlalchemy.orm import Session
from app.dto.core.common import UploadFileRequest
from app.dto.core.file import GetFileDBResponse, GetListFileResponse, UploadFileResponse
from app.helper.base_response import DataResponse, PagingDataResponse
from app.helper.db import db_session
from app.service import common_service
from app.service.file import FileService
from app.util.openapi import map_resp_to_openapi



router = APIRouter()

_logger = logging.getLogger(__name__)



@router.post('/upload-file', response_model=DataResponse[UploadFileResponse])
def upload_document_file(*, upload_file_request: UploadFileRequest = File(...)):
    data = common_service.upload_file(user_id=3 ,file=upload_file_request)
    return DataResponse().success_response(data=data)


@router.get('/', response_model=DataResponse[GetFileDBResponse])
def get_file(db: Session = Depends(db_session),
                                  *, id: int):
    data = FileService.get_file(db, id=id)
    return DataResponse().success_response(data=data)


@router.get('/list-file', response_model=PagingDataResponse[GetListFileResponse])
def get_list_file(db: Session = Depends(db_session),
                                  *, user_id: Optional[int] = None):
    data, pagination = FileService.get_list_file(db, user_id=user_id)
    return PagingDataResponse().success_response(data=data, pagination=pagination)
