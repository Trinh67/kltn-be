import logging
from typing import Optional
from fastapi import APIRouter, Depends, File, Form
from sqlalchemy.orm import Session
from app.dto.core.common import UploadFileRequest
from app.dto.core.file import GetFileResponse, GetListFileResponse
from app.helper.base_response import DataResponse
from app.helper.db import db_session
from app.service.file import FileService
from app.util.openapi import map_resp_to_openapi



router = APIRouter()

_logger = logging.getLogger(__name__)


@router.get('/', response_model=DataResponse[GetFileResponse])
def get_file(db: Session = Depends(db_session),
                                  *, id: int):
    data = FileService.get_file(db, id=id)
    return DataResponse().success_response(data=data)


@router.get('/list-file', response_model=DataResponse[GetListFileResponse])
def get_list_file(db: Session = Depends(db_session),
                                  *, user_id: int):
    data = FileService.get_list_file(db, user_id=user_id)
    return DataResponse().success_response(data=data)
