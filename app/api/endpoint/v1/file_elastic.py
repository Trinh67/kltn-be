import logging
from typing import Optional
from fastapi import APIRouter, Depends, File, Form
from sqlalchemy.orm import Session
from app.dto.base import OpenApiResponseModel
from app.dto.core.common import UploadFileRequest
from app.dto.core.file import SearchFileMappingResponse
from app.helper.base_response import DataResponse, PagingDataResponse
from app.helper.db import db_session
from app.service import common_service
from app.service.file_elastic import FileElasticService
from app.util.openapi import map_resp_to_openapi

from app.dto.core.file_elastic import CreateFileRequest, CreateFileResponse, GetFileResponse, GetListFileResponse, SearchFileRequest, UploadFileResponse


router = APIRouter()

_logger = logging.getLogger(__name__)


@router.post('/upload-file', response_model=DataResponse[UploadFileResponse])
def upload_document_file(*, upload_file_request: UploadFileRequest = File(...), user_id: int = Form(..., alias='userId')):
    data = common_service.upload_file(user_id=user_id ,file=upload_file_request)
    return DataResponse().success_response(data=data)


@router.post("/", response_model=DataResponse[CreateFileResponse],
             response_description="Success",
             responses=map_resp_to_openapi([
                 OpenApiResponseModel(code=402, message='Param {param} is required', http_code='400',
                                      description='Missing required param'),
                 OpenApiResponseModel(code=404, message='{Object} not found', http_code='400',
                                      description='Object not found eg: campaign'),
                 OpenApiResponseModel(code=417, message='{param} format is invalid', http_code='400',
                                      description='File path format is invalid'),
             ]))
def create_file(db: Session = Depends(db_session),
                                  *,
                                  request_input: CreateFileRequest):
    data = FileElasticService.create_file(db, request_input=request_input)
    return DataResponse().success_response(data=data)


@router.get('/', response_model=DataResponse[GetFileResponse])
def get_file(id: str):
    data = FileElasticService.get_file(id=id)
    return DataResponse().success_response(data=data)


@router.get('/list-file', response_model=DataResponse[GetListFileResponse])
def get_list_file(size: int = 5):
    data = FileElasticService.get_list_file(size = size)
    return DataResponse().success_response(data=data)


@router.post('/search', response_model=DataResponse[SearchFileMappingResponse])
def search_content_file(db: Session = Depends(db_session),
                                  *,
                                  request_input: SearchFileRequest):
    data, pagination = FileElasticService.search_content(db, request_input)
    return PagingDataResponse().success_response(data=data, pagination=pagination)